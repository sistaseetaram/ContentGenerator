#!/usr/bin/env python3
"""
YouTube upload tool — Setu content pipeline.

Usage:
    python tools/youtube_upload.py \
        --file path/to/video.mp4 \
        --title "Video title" \
        --description "Description text" \
        --tags "n8n,automation,buildinpublic" \
        --privacy public

First run: opens browser for Google OAuth consent. Token saved to
.youtube_token.json — all subsequent runs skip the browser.
"""

import argparse
import json
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # comments, replies, analytics
    "https://www.googleapis.com/auth/youtube.readonly",   # read channel/video data
]

_default_secrets = os.path.join(os.path.dirname(__file__), "..", "youtube_client_secrets.json")
_default_token = os.path.join(os.path.dirname(__file__), "..", ".youtube_token.json")

SECRETS_FILE = os.environ.get("YOUTUBE_CLIENT_SECRETS_PATH", _default_secrets)
TOKEN_FILE = os.environ.get("YOUTUBE_TOKEN_PATH", _default_token)


def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(SECRETS_FILE):
                print(f"ERROR: client secrets not found at {SECRETS_FILE}")
                print("Download it from Google Cloud Console → Credentials → your OAuth client → Download JSON")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def upload_video(file_path, title, description, tags, privacy):
    if not os.path.exists(file_path):
        print(f"ERROR: file not found: {file_path}")
        sys.exit(1)

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "categoryId": "28",  # Science & Technology
        },
        "status": {
            "privacyStatus": privacy,
            "madeForKids": False,
        },
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    print(f"Uploading: {os.path.basename(file_path)}")
    print(f"Title: {title}")
    print(f"Privacy: {privacy}")
    print()

    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"  {pct}% uploaded...", end="\r")

    video_id = response["id"]
    url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"\nDone. Video URL: {url}")
    return url


def main():
    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument("--file", required=True, help="Path to video file")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    args = parser.parse_args()

    url = upload_video(args.file, args.title, args.description, args.tags, args.privacy)

    # Write URL to a temp file so other scripts can read it
    out = os.path.join(os.path.dirname(__file__), "..", ".tmp", "last_yt_upload.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(url)


if __name__ == "__main__":
    main()
