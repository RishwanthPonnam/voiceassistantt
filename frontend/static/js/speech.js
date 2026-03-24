// Text-to-Speech Implementation
const speechSynthesis = window.speechSynthesis;

function speakText(text) {
    // Cancel any ongoing speech
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Configure speech properties
    utterance.rate = 1.0;        // Speed of speech
    utterance.pitch = 1.0;       // Pitch of voice
    utterance.volume = 1.0;      // Volume level

    // Optional: Select voice
    const voices = speechSynthesis.getVoices();
    if (voices.length > 0) {
        utterance.voice = voices[0]; // Use first available voice
    }

    // Event handlers
    utterance.onstart = function() {
        console.log('Speech started');
    };

    utterance.onend = function() {
        console.log('Speech ended');
    };

    utterance.onerror = function(event) {
        console.error('Speech synthesis error:', event.error);
    };

    // Speak the text
    speechSynthesis.speak(utterance);
}

function stopSpeech() {
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }
}

// Load voices when they're available
speechSynthesis.onvoiceschanged = function() {
    console.log('Voices loaded:', speechSynthesis.getVoices().length);
};

// Auto-load voices
window.addEventListener('load', function() {
    // Trigger voice loading
    speechSynthesis.getVoices();
});
