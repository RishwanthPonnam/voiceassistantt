// Speech Recognition Implementation
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let isListening = false;

function initializeSpeechRecognition() {
    if (!SpeechRecognition) {
        console.error('Speech Recognition API not supported in this browser');
        showSystemMessage('⚠️ Speech recognition not supported in your browser. Please use Chrome, Firefox, or Edge.');
        logDebug('❌ Speech Recognition API not available', 'error');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.language = 'en-US';

    logDebug('✓ Speech Recognition initialized', 'info');

    recognition.onstart = function() {
        isListening = true;
        updateVoiceButtonUI();
        showSystemMessage('🎤 Listening... Speak now!');
        logDebug('🎤 Recording started', 'info');
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
        
        if (!isFinal) {
            logDebug(`📝 Interim: "${transcript}"`, 'info');
        }
        
        // If final result, process it
        if (isFinal) {
            logDebug(`✓ Final result: "${transcript}"`, 'info');
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
        logDebug(`❌ Error: ${event.error}`, 'error');
        isListening = false;
        updateVoiceButtonUI();
    };

    recognition.onend = function() {
        isListening = false;
        updateVoiceButtonUI();
        logDebug('⏹️ Recording stopped', 'info');
    };
}

function toggleVoiceRecording() {
    if (!recognition) {
        logDebug('⚠️ Recognition not initialized, initializing now...', 'warn');
        initializeSpeechRecognition();
    }

    if (isListening) {
        recognition.stop();
        showSystemMessage('🛑 Stopped listening.');
        logDebug('🛑 User stopped recording', 'info');
    } else {
        document.getElementById('messageInput').value = '';
        try {
            recognition.start();
            logDebug('🎤 Starting voice recognition...', 'info');
        } catch (e) {
            console.error('Error starting recognition:', e);
            showSystemMessage('❌ Error starting voice input. Please try again.');
            logDebug(`❌ Error starting recognition: ${e.message}`, 'error');
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
