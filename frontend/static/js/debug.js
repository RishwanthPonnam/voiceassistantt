// Debug Console
let debugMode = false;

function initDebugConsole() {
    const debugToggle = document.getElementById('debugToggle');
    const debugClose = document.getElementById('debugClose');
    const debugClear = document.getElementById('debugClear');
    const debugConsole = document.getElementById('debugConsole');

    // Toggle debug console
    debugToggle.addEventListener('click', () => {
        debugMode = !debugMode;
        debugConsole.style.display = debugMode ? 'block' : 'none';
        logDebug('🔧 Debug console ' + (debugMode ? 'opened' : 'closed'));
    });

    // Close debug console
    debugClose.addEventListener('click', () => {
        debugMode = false;
        debugConsole.style.display = 'none';
    });

    // Clear log
    debugClear.addEventListener('click', () => {
        const debugLog = document.getElementById('debugLog');
        debugLog.innerHTML = '<p class="debug-info">Log cleared...</p>';
    });

    // Log initial info
    logDebug('🎯 Voice Assistant Debug Console Initialized');
    logDebug('🌐 Server URL: ' + window.location.origin);
    logDebug('🎤 Speech Recognition: ' + (window.SpeechRecognition ? '✓ Available' : '✗ Not Available'));
    logDebug('🔊 Speech Synthesis: ' + (window.speechSynthesis ? '✓ Available' : '✗ Not Available'));
}

function logDebug(message, type = 'info') {
    const debugLog = document.getElementById('debugLog');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('p');
    logEntry.className = `debug-${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    
    debugLog.appendChild(logEntry);
    debugLog.scrollTop = debugLog.scrollHeight;
    
    // Also log to browser console
    console[type === 'error' ? 'error' : type === 'warn' ? 'warn' : 'log'](message);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initDebugConsole);

// Intercept console logs
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;

console.log = function(...args) {
    originalLog.apply(console, args);
    if (debugMode) {
        logDebug(args.join(' '), 'info');
    }
};

console.error = function(...args) {
    originalError.apply(console, args);
    if (debugMode) {
        logDebug(args.join(' '), 'error');
    }
};

console.warn = function(...args) {
    originalWarn.apply(console, args);
    if (debugMode) {
        logDebug(args.join(' '), 'warn');
    }
};
