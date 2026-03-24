// Command handling
document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voiceBtn');
    const sendBtn = document.getElementById('sendBtn');
    const messageInput = document.getElementById('messageInput');

    // Voice Button Click
    voiceBtn.addEventListener('click', function() {
        if (typeof toggleVoiceRecording === 'function') {
            toggleVoiceRecording();
        } else {
            showSystemMessage('❌ Voice recognition not initialized. Please refresh the page.');
        }
    });

    // Send Button Click
    sendBtn.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            processUserInput(message);
            messageInput.value = '';
        } else {
            showSystemMessage('⚠️ Please enter a message or use voice input.');
        }
    });

    // Enter Key for Send
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const message = messageInput.value.trim();
            if (message) {
                processUserInput(message);
                messageInput.value = '';
            }
        }
    });

    // Show welcome message
    setTimeout(() => {
        showSystemMessage('👋 Welcome! Try saying "open whatsapp" or "what time is it?"');
    }, 500);
});

function processUserInput(message) {
    // Display user message
    addMessageToChat(message, 'user-message');

    // Send to backend
    fetch('/api/voice/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            command: message
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            addMessageToChat(data.response, 'assistant-message');
            
            // Optional: Synthesize speech response
            if (typeof speakText === 'function') {
                speakText(data.response);
            }
            
            // Save to message history
            if (typeof saveMessage === 'function') {
                saveMessage(message, data.response);
            }
        } else {
            const errorMsg = data.error || 'An unknown error occurred';
            addMessageToChat('❌ Error: ' + errorMsg, 'assistant-message');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('❌ Communication error. Please check that the server is running at localhost:5000', 'assistant-message');
    });
}

function addMessageToChat(text, className) {
    const chatbox = document.getElementById('chatbox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    messageDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function showSystemMessage(text) {
    const chatbox = document.getElementById('chatbox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system-message';
    messageDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
