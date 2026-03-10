// Sign Language Transcriber - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupSmoothScroll();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(button => {
        button.addEventListener('click', handleButtonClick);
    });
}

/**
 * Handle button clicks
 */
function handleButtonClick(e) {
    const text = e.target.textContent;
    
    if (text.includes('Get Started') || text.includes('Launch')) {
        console.log('Launching transcriber app...');
        // TODO: Navigate to transcriber page or open modal
    } else if (text.includes('Learn More')) {
        console.log('Scrolling to features...');
        document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Setup smooth scroll behavior for navigation links
 */
function setupSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

/**
 * Example function for transcription API call
 */
async function transcribeSign(videoData) {
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video: videoData
            })
        });
        
        const result = await response.json();
        console.log('Transcription result:', result);
        return result;
    } catch (error) {
        console.error('Error during transcription:', error);
    }
}
