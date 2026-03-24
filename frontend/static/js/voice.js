// Speech Recognition Implementation
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let isListening = false;

function initializeSpeechRecognition() {
    if (!SpeechRecognition) {
        console.error('Speech Recognition API not supported in this browser');
        showSystemMessage('Speech recognition not supported in your browser');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.language = 'en-US';

    recognition.onstart = function() {
        isListening = true;
        updateVoiceButtonUI();
    };

    recognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }

        if (event.isFinal) {
            document.getElementById('messageInput').value = transcript;
            processUserInput(transcript);
        }
    };

    recognition.onerror = function(event) {
        console.error('Speech Recognition Error:', event.error);
        showSystemMessage('Error during voice input: ' + event.error);
        isListening = false;
        updateVoiceButtonUI();
    };

    recognition.onend = function() {
        isListening = false;
        updateVoiceButtonUI();
    };
}

function toggleVoiceRecording() {
    if (!recognition) {
        initializeSpeechRecognition();
    }

    if (isListening) {
        recognition.stop();
    } else {
        document.getElementById('messageInput').value = '';
        recognition.start();
    }
}

function updateVoiceButtonUI() {
    const btn = document.getElementById('voiceBtn');
    const icon = document.getElementById('voiceIcon');
    
    if (isListening) {
        btn.classList.add('recording');
        icon.textContent = '⏹️';
        btn.textContent = '⏹️ Stop Recording';
    } else {
        btn.classList.remove('recording');
        icon.textContent = '🎤';
        btn.childNodes[1].textContent = 'Start Recording';
    }
}

// Initialize speech recognition when page loads
document.addEventListener('DOMContentLoaded', initializeSpeechRecognition);
