"""
Model router with fallback chains, cost logging, and daily Claude budget guard.
Every model call in ContentGenerator goes through route(). Never call SDKs directly.

Usage:
    from tools.model_router import route
    result = route("long-form", "Write a LinkedIn post about...", system="You are...")
    print(result["content"])
"""

import json
import os
import time
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
SPEND_FILE = ROOT / "data" / "model_spend.json"

FAILOVER_TRIGGERS = {429, 529, 503, 500, 504}
RETRY_BUDGET = 1
QUOTA_GUARD_USD_PER_DAY = 5.0
LATENCY_BUDGET_SECONDS = 60

# Cost per 1M tokens (input / output) in USD — update on Day-7 revisit
COST_PER_TOKEN = {
    "claude-sonnet-4-6":    (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-haiku-4-5":     (0.80 / 1_000_000,  4.00 / 1_000_000),
    "gpt-4o":               (5.00 / 1_000_000, 15.00 / 1_000_000),
    "gpt-4o-mini":          (0.15 / 1_000_000,  0.60 / 1_000_000),
    "gemini-2.5-flash":     (0.30 / 1_000_000,   2.50 / 1_000_000),  # free tier at low volume
    "deepseek-chat":        (0.27 / 1_000_000,  1.10 / 1_000_000),
    "groq-llama-3.3-70b":   (0.00 / 1_000_000,  0.00 / 1_000_000),  # free tier
    "gemma4-12b":           (0.00 / 1_000_000,  0.00 / 1_000_000),  # local Ollama — free
    "whisper-1":            (0.006/ 60, 0.0),                         # per minute of audio
    "deepgram-nova-3":      (0.0043/ 60, 0.0),
    "assemblyai":           (0.0062/ 60, 0.0),
    "text-embedding-3-small":(0.02 / 1_000_000, 0.0),
    "voyage-3":             (0.06 / 1_000_000, 0.0),
    "cohere-embed-v3":      (0.10 / 1_000_000, 0.0),
}

CLAUDE_MODELS = {"claude-sonnet-4-6", "claude-haiku-4-5"}

# Fallback chains per task type. Primary is index 0.
CHAINS = {
    "long-form":    ["gemini-2.5-flash", "gpt-4o", "claude-sonnet-4-6"],
    "short-post":   ["gpt-4o-mini", "gemini-2.5-flash", "claude-haiku-4-5"],
    "multimodal":   ["gemini-2.5-flash", "gpt-4o", "claude-sonnet-4-6"],
    "transcription":["whisper-1", "deepgram-nova-3", "assemblyai"],
    "lint-dispatch":["claude-haiku-4-5", "gpt-4o-mini", "groq-llama-3.3-70b"],
    "auditor":      ["gemini-2.5-flash", "gpt-4o", "claude-sonnet-4-6"],
    "yt-summarize": ["deepseek-chat", "gpt-4o-mini", "gemini-2.5-flash"],
    # Bulk research summarize — free model first to zero out fan-out cost. Never Claude.
    "research-summarize": ["groq-llama-3.3-70b", "gemini-2.5-flash", "deepseek-chat"],
    "embedding":    ["text-embedding-3-small", "voyage-3", "cohere-embed-v3"],
    # Local Gemma 4 12B — zero cost, offline, private. Primary for classification/routing tasks.
    "tagging":        ["gemma4-12b", "groq-llama-3.3-70b", "gemini-2.5-flash"],
    "classification": ["gemma4-12b", "groq-llama-3.3-70b", "gemini-2.5-flash"],
    "scoring":        ["gemma4-12b", "groq-llama-3.3-70b", "claude-haiku-4-5"],
    "routing":        ["gemma4-12b", "groq-llama-3.3-70b", "claude-haiku-4-5"],
}


class ModelRouterExhausted(Exception):
    """All models in fallback chain failed."""


def _today_claude_spend() -> float:
    """Sum today's Claude-only costs from model_spend.json."""
    today = str(date.today())
    if not SPEND_FILE.exists():
        return 0.0
    try:
        data = json.loads(SPEND_FILE.read_text())
        return sum(
            e.get("cost_usd", 0)
            for e in data.get("daily", {}).get(today, [])
            if e.get("model_used") in CLAUDE_MODELS
        )
    except (json.JSONDecodeError, AttributeError):
        return 0.0


def _log_call(entry: dict) -> None:
    """Append a call record to data/model_spend.json."""
    today = str(date.today())
    SPEND_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SPEND_FILE.exists():
        try:
            data = json.loads(SPEND_FILE.read_text())
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    data.setdefault("daily", {}).setdefault(today, []).append(entry)
    data.setdefault("by_model", {}).setdefault(entry["model_used"], []).append(entry)
    data.setdefault("by_skill", {}).setdefault(entry.get("task_type", "unknown"), []).append(entry)

    SPEND_FILE.write_text(json.dumps(data, indent=2))


def _estimate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    rates = COST_PER_TOKEN.get(model, (0.0, 0.0))
    return tokens_in * rates[0] + tokens_out * rates[1]


def _call_anthropic(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=model,
        max_tokens=kwargs.get("max_tokens", 2048),
        system=system or "You are a helpful assistant.",
        messages=messages,
    )
    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens
    content = response.content[0].text
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_openai(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 2048),
    )
    tokens_in = response.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens
    content = response.choices[0].message.content
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_gemini(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(full_prompt)
    content = response.text
    # Gemini doesn't always expose token counts in basic API — estimate
    tokens_in = len(full_prompt.split()) * 4 // 3
    tokens_out = len(content.split()) * 4 // 3
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_deepseek(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 2048),
    )
    tokens_in = response.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens
    content = response.choices[0].message.content
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_local_ollama(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
    ollama_model = {"gemma4-12b": "gemma4:12b"}.get(model, model)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 2048),
    )
    tokens_in = response.usage.prompt_tokens if response.usage else 0
    tokens_out = response.usage.completion_tokens if response.usage else 0
    content = response.choices[0].message.content
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_groq(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    from groq import Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 2048),
    )
    tokens_in = response.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens
    content = response.choices[0].message.content
    return {"content": content, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _dispatch(model: str, prompt: str, system: str = "", **kwargs) -> dict:
    """Call the right SDK based on model name."""
    if model.startswith("claude-"):
        return _call_anthropic(model, prompt, system, **kwargs)
    elif model in ("gpt-4o", "gpt-4o-mini", "text-embedding-3-small"):
        return _call_openai(model, prompt, system, **kwargs)
    elif model.startswith("gemini-"):
        return _call_gemini(model, prompt, system, **kwargs)
    elif model == "deepseek-chat":
        return _call_deepseek(model, prompt, system, **kwargs)
    elif model.startswith("groq-"):
        return _call_groq(model, prompt, system, **kwargs)
    elif model.startswith("gemma4-"):
        return _call_local_ollama(model, prompt, system, **kwargs)
    else:
        raise ValueError(f"No dispatcher for model: {model}")


def route(task_type: str, prompt: str, system: str = "", **kwargs) -> dict:
    """
    Route a task through the appropriate model chain with failover.

    Returns dict with keys: content, model_used, fallback_depth, tokens_in, tokens_out,
    cost_usd, latency_s, task_type.

    Raises ModelRouterExhausted if all models in chain fail.
    """
    if task_type not in CHAINS:
        raise ValueError(f"Unknown task_type '{task_type}'. Valid: {list(CHAINS)}")

    chain = list(CHAINS[task_type])

    # Budget guard: if today's Claude spend >= limit, remove Claude models from chain
    if _today_claude_spend() >= QUOTA_GUARD_USD_PER_DAY:
        chain = [m for m in chain if m not in CLAUDE_MODELS]
        if not chain:
            raise ModelRouterExhausted(
                f"Claude daily budget ({QUOTA_GUARD_USD_PER_DAY} USD) reached "
                "and no non-Claude fallback available."
            )

    last_error = None
    for depth, model in enumerate(chain):
        t_start = time.monotonic()
        try:
            result = _dispatch(model, prompt, system, **kwargs)
            latency = time.monotonic() - t_start

            tokens_in = result.get("tokens_in", 0)
            tokens_out = result.get("tokens_out", 0)
            cost = _estimate_cost(model, tokens_in, tokens_out)

            entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "task_type": task_type,
                "model_used": model,
                "fallback_depth": depth,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "cost_usd": round(cost, 6),
                "latency_s": round(latency, 2),
            }
            _log_call(entry)

            return {
                "content": result["content"],
                "model_used": model,
                "fallback_depth": depth,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "cost_usd": cost,
                "latency_s": latency,
                "task_type": task_type,
            }

        except Exception as exc:
            last_error = exc
            # Check if this is a failover-triggerable HTTP error
            status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
            if status not in FAILOVER_TRIGGERS:
                # Non-retriable error (auth, bad request, etc.) — don't try next model
                raise
            # Retriable — try next in chain
            continue

    raise ModelRouterExhausted(
        f"All models exhausted for task_type='{task_type}'. "
        f"Last error: {last_error}"
    )
