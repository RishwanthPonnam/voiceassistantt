// Speech Recognition Implementation
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let isListening = false;

function initializeSpeechRecognition() {
    if (!SpeechRecognition) {
        console.error('Speech Recognition API not supported in this browser');
        showSystemMessage('⚠️ Speech recognition not supported in your browser. Please use Chrome, Firefox, or Edge.');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.language = 'en-US';

    recognition.onstart = function() {
        isListening = true;
        updateVoiceButtonUI();
        showSystemMessage('🎤 Listening... Speak now!');
    };

    recognition.onresult = function(event) {
        let transcript = '';
        let isFinal = false;
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                isFinal = true;
            }
        }

        // Show interim results in input field
        document.getElementById('messageInput').value = transcript;
        
        // If final result, process it
        if (isFinal) {
            setTimeout(() => {
                processUserInput(transcript);
            }, 500);
        }
    };

    recognition.onerror = function(event) {
        console.error('Speech Recognition Error:', event.error);
        let errorMsg = '❌ Voice input error: ' + event.error;
        
        if (event.error === 'no-speech') {
            errorMsg = '❌ No speech detected. Please try again and speak clearly.';
        } else if (event.error === 'network') {
            errorMsg = '❌ Network error. Check your internet connection.';
        }
        
        showSystemMessage(errorMsg);
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
        showSystemMessage('🛑 Stopped listening.');
    } else {
        document.getElementById('messageInput').value = '';
        try {
            recognition.start();
        } catch (e) {
            console.error('Error starting recognition:', e);
            showSystemMessage('❌ Error starting voice input. Please try again.');
        }
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
        btn.textContent = '🎤 Start Recording';
    }
}

// Initialize speech recognition when page loads
document.addEventListener('DOMContentLoaded', initializeSpeechRecognition);
