// LinkedIn Carousel Slides Data
let slides = [
    {
        id: 1,
        headline: "Same project. Third version. Finally makes sense.",
        body: "V1: one massive prompt, $1/run.\nV2: subworkflows & split prompts.\n\nNow, V3 handles verification before fetching. The model only sees what it needs.",
        theme: "terracotta",
        isCover: true,
        visualType: "none",
        visualContent: "",
        showProfileHeader: true
    },
    {
        id: 2,
        headline: "The Evolution of an Automation",
        body: "I spent weeks following tutorials. Built every template. Understood nothing—because their data flows weren't breaking. Mine weren't either, because they weren't mine.",
        theme: "anthracite",
        isCover: false,
        visualType: "text-large",
        visualContent: "The frustration is the curriculum.",
        showProfileHeader: true
    },
    {
        id: 3,
        headline: "V3 Architecture Canvas",
        body: "Data mapping errors, variable names pointing nowhere, infinite loops. That is the actual class. Here is the resulting n8n production flow.",
        theme: "light",
        isCover: false,
        visualType: "image",
        visualContent: "assets/screenshot1.png",
        showProfileHeader: false
    },
    {
        id: 4,
        headline: "Seamless Chat Delivery",
        body: "The workflow is controlled via a simple Telegram trigger, allowing on-demand stock queries, parameter overrides, and immediate PDF delivery.",
        theme: "light",
        isCover: false,
        visualType: "image",
        visualContent: "assets/screenshot2.png",
        showProfileHeader: false
    },
    {
        id: 5,
        headline: "The Output PDF Report",
        body: "When the analysis completes, a multi-page PDF report is generated containing deep financial stats and news context, and returned to the user.",
        theme: "light",
        isCover: false,
        visualType: "image",
        visualContent: "assets/document_preview.png",
        showProfileHeader: false
    },
    {
        id: 6,
        headline: "The Payoff: $0.06 Per Report",
        body: "Nobody ships a good automation on the first try. Most tutorials show the finished thing. They skip the three versions before it.\n\nV4 is coming.",
        theme: "terracotta",
        isCover: false,
        visualType: "text-large",
        visualContent: "What version are you on?",
        showProfileHeader: true
    },
    {
        id: 7,
        headline: "Build in Public.",
        body: "Follow the journey as we build Setu, an AI automation agency focused on real hours, real money, and outcome-first engineering.",
        theme: "forest",
        isCover: false,
        visualType: "wordmark",
        visualContent: "",
        showProfileHeader: false
    }
];

let activeSlideIndex = 0;
let isPrintLayout = false;

// DOM Elements
const slideCanvas = document.getElementById('slide-canvas');
const slideSelect = document.getElementById('slide-select');
const headlineInput = document.getElementById('slide-headline-input');
const bodyInput = document.getElementById('slide-body-input');
const wordCountDisplay = document.getElementById('word-count');
const visualContainer = document.getElementById('slide-visual');
const prevBtn = document.getElementById('prev-slide');
const nextBtn = document.getElementById('next-slide');
const copyPostBtn = document.getElementById('copy-post-btn');
const toggleViewBtn = document.getElementById('toggle-view-mode');
const carouselViewer = document.getElementById('carousel-viewer');
const printStack = document.getElementById('print-stack');
const printSlidesContainer = document.querySelector('.print-slides-container');
const themeButtons = document.querySelectorAll('.theme-btn');
const toast = document.getElementById('toast');
const profileHeaderCheckbox = document.getElementById('show-profile-header-input');

// Initialize
function init() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('print') === 'true') {
        isPrintLayout = true;
        rebuildPrintStack();
        carouselViewer.classList.add('hidden');
        printStack.classList.remove('hidden');
        toggleViewBtn.innerHTML = '<span class="icon">🖼️</span> Toggle Slide Viewer';
    }
    renderSlide();
    setupEventListeners();
    updateInputs();
}

// Render active slide to the canvas
function renderSlide() {
    const slide = slides[activeSlideIndex];
    
    // Set theme background class
    slideCanvas.className = `slide-canvas theme-${slide.theme}`;
    if (slide.isCover) {
        slideCanvas.classList.add('cover-slide');
    }
    
    // Set text elements
    const headlineElem = slideCanvas.querySelector('.slide-headline');
    const bodyElem = slideCanvas.querySelector('.slide-body-text');
    const numDisplay = slideCanvas.querySelector('.slide-number-display');
    
    headlineElem.textContent = slide.headline;
    bodyElem.textContent = slide.body;
    numDisplay.textContent = `${activeSlideIndex + 1} / ${slides.length}`;
    
    // Render profile header if enabled
    const profileHeaderContainer = slideCanvas.querySelector('#slide-profile-header-container');
    if (slide.showProfileHeader) {
        profileHeaderContainer.innerHTML = `
            <div class="profile-header">
                <img src="assets/setu-founder.png" class="profile-avatar" alt="Sista Seetaram">
                <div class="profile-info">
                    <div class="profile-name-container">
                        <span class="profile-name">Sista Seetaram</span>
                        <span class="profile-badge">
                            <svg viewBox="0 0 24 24">
                                <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                        </span>
                    </div>
                    <span class="profile-handle">Founder @ Setu · I help businesses find where AI pays them back</span>
                </div>
            </div>
        `;
    } else {
        profileHeaderContainer.innerHTML = '';
    }
    
    // Render visual element based on type
    visualContainer.innerHTML = '';
    visualContainer.className = 'slide-visual-container';
    
    if (slide.visualType === 'image') {
        const img = document.createElement('img');
        img.src = slide.visualContent;
        img.alt = slide.headline;
        visualContainer.appendChild(img);
    } else if (slide.visualType === 'pdf') {
        const embed = document.createElement('iframe');
        embed.src = slide.visualContent;
        visualContainer.appendChild(embed);
    } else if (slide.visualType === 'text-large') {
        const textDiv = document.createElement('div');
        textDiv.style.fontFamily = "'Cormorant Garamond', serif";
        textDiv.style.fontSize = "26px";
        textDiv.style.fontStyle = "italic";
        textDiv.style.opacity = "0.9";
        textDiv.style.textAlign = "center";
        textDiv.style.padding = "10px";
        textDiv.textContent = slide.visualContent;
        visualContainer.appendChild(textDiv);
    } else if (slide.visualType === 'wordmark') {
        const wordmarkDiv = document.createElement('div');
        wordmarkDiv.className = 'setu-wordmark';
        wordmarkDiv.style.fontSize = "54px";
        wordmarkDiv.innerHTML = '<span class="deva">से</span><span class="latin">tu</span>';
        visualContainer.appendChild(wordmarkDiv);
        visualContainer.style.background = 'none';
    } else {
        // No visual
        visualContainer.classList.add('hidden');
    }
    
    // Update theme picker active status
    themeButtons.forEach(btn => {
        if (btn.getAttribute('data-color') === getThemeHex(slide.theme)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Translate theme name to hex
function getThemeHex(themeName) {
    const map = {
        'terracotta': '#1e0f09',
        'light': '#ffffff',
        'forest': '#0e1810',
        'anthracite': '#222222'
    };
    return map[themeName] || '#ffffff';
}

// Translate hex back to theme name
function getThemeName(hex) {
    const map = {
        '#1e0f09': 'terracotta',
        '#ffffff': 'light',
        '#0e1810': 'forest',
        '#222222': 'anthracite'
    };
    return map[hex] || 'light';
}

// Update the controls values in the sidebar
function updateInputs() {
    const slide = slides[activeSlideIndex];
    slideSelect.value = (activeSlideIndex + 1).toString();
    headlineInput.value = slide.headline;
    bodyInput.value = slide.body;
    profileHeaderCheckbox.checked = !!slide.showProfileHeader;
    
    // Count words in body
    const words = slide.body.trim().split(/\s+/).filter(w => w.length > 0).length;
    wordCountDisplay.textContent = words;
    if (words > 25) {
        wordCountDisplay.style.color = '#ff6b6b';
    } else {
        wordCountDisplay.style.color = 'var(--text-secondary)';
    }
}

// Rebuild the stacked print view
function rebuildPrintStack() {
    printSlidesContainer.innerHTML = '';
    slides.forEach((slide, idx) => {
        const slideClone = document.createElement('div');
        slideClone.className = `slide-canvas theme-${slide.theme}`;
        if (slide.isCover) slideClone.classList.add('cover-slide');
        
        // Inner markup
        let visualHTML = '';
        if (slide.visualType === 'image') {
            visualHTML = `<div class="slide-visual-container"><img src="${slide.visualContent}" alt="${slide.headline}"></div>`;
        } else if (slide.visualType === 'pdf') {
            visualHTML = `<div class="slide-visual-container"><iframe src="${slide.visualContent}"></iframe></div>`;
        } else if (slide.visualType === 'text-large') {
            visualHTML = `<div class="slide-visual-container" style="background:rgba(0,0,0,0.02)"><div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-style:italic;opacity:0.9;text-align:center;padding:10px;">${slide.visualContent}</div></div>`;
        } else if (slide.visualType === 'wordmark') {
            visualHTML = `<div class="slide-visual-container" style="background:none"><div class="setu-wordmark" style="font-size:54px;"><span class="deva">से</span><span class="latin">tu</span></div></div>`;
        }
        
        let profileHeaderHTML = '';
        if (slide.showProfileHeader) {
            profileHeaderHTML = `
                <div class="profile-header">
                    <img src="assets/setu-founder.png" class="profile-avatar" alt="Sista Seetaram">
                    <div class="profile-info">
                        <div class="profile-name-container">
                            <span class="profile-name">Sista Seetaram</span>
                            <span class="profile-badge">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                </svg>
                            </span>
                        </div>
                        <span class="profile-handle">Founder @ Setu · I help businesses find where AI pays them back</span>
                    </div>
                </div>
            `;
        }
        
        slideClone.innerHTML = `
            <div class="slide-content">
                <div class="slide-header">
                    <span class="slide-tag">SETU BUILD RECEIPTS</span>
                </div>
                <div class="slide-body">
                    ${profileHeaderHTML}
                    <h2 class="slide-headline">${slide.headline}</h2>
                    <p class="slide-body-text">${slide.body.replace(/\n/g, '<br>')}</p>
                    ${visualHTML}
                </div>
                <div class="slide-footer">
                    <span class="brand-wordmark setu-wordmark"><span class="deva">से</span><span class="latin">tu</span></span>
                    <span class="slide-number-display">${idx + 1} / ${slides.length}</span>
                </div>
            </div>
        `;
        printSlidesContainer.appendChild(slideClone);
    });
}

// Setup events
function setupEventListeners() {
    // Dropdown change
    slideSelect.addEventListener('change', (e) => {
        activeSlideIndex = parseInt(e.target.value) - 1;
        renderSlide();
        updateInputs();
    });
    
    // Headline edit
    headlineInput.addEventListener('input', (e) => {
        slides[activeSlideIndex].headline = e.target.value;
        renderSlide();
    });
    
    // Profile header toggle
    profileHeaderCheckbox.addEventListener('change', (e) => {
        slides[activeSlideIndex].showProfileHeader = e.target.checked;
        renderSlide();
    });
    
    // Body edit
    bodyInput.addEventListener('input', (e) => {
        slides[activeSlideIndex].body = e.target.value;
        renderSlide();
        
        // Count words
        const words = e.target.value.trim().split(/\s+/).filter(w => w.length > 0).length;
        wordCountDisplay.textContent = words;
        if (words > 25) {
            wordCountDisplay.style.color = '#ff6b6b';
        } else {
            wordCountDisplay.style.color = 'var(--text-secondary)';
        }
    });
    
    // Theme buttons
    themeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const hex = e.target.getAttribute('data-color');
            const themeName = getThemeName(hex);
            slides[activeSlideIndex].theme = themeName;
            
            // Toggle active visual indicator
            themeButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            renderSlide();
        });
    });
    
    // Navigation arrows
    prevBtn.addEventListener('click', () => {
        if (activeSlideIndex > 0) {
            activeSlideIndex--;
            renderSlide();
            updateInputs();
        }
    });
    
    nextBtn.addEventListener('click', () => {
        if (activeSlideIndex < slides.length - 1) {
            activeSlideIndex++;
            renderSlide();
            updateInputs();
        }
    });
    
    // Copy Post Text
    copyPostBtn.addEventListener('click', () => {
        const text = document.getElementById('linkedin-post-text').textContent;
        navigator.clipboard.writeText(text).then(() => {
            showToast('LinkedIn Post Copied!');
        });
    });
    
    // Toggle View/Print Layout
    toggleViewBtn.addEventListener('click', () => {
        isPrintLayout = !isPrintLayout;
        if (isPrintLayout) {
            rebuildPrintStack();
            carouselViewer.classList.add('hidden');
            printStack.classList.remove('hidden');
            toggleViewBtn.innerHTML = '<span class="icon">🖼️</span> Toggle Slide Viewer';
        } else {
            carouselViewer.classList.remove('hidden');
            printStack.classList.add('hidden');
            toggleViewBtn.innerHTML = '<span class="icon">📄</span> Toggle Print Layout';
        }
    });
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 2500);
}

// Run
window.addEventListener('DOMContentLoaded', init);
