// Command handling
document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voiceBtn');
    const sendBtn = document.getElementById('sendBtn');
    const messageInput = document.getElementById('messageInput');

    // Voice Button Click
    voiceBtn.addEventListener('click', function() {
        if (typeof toggleVoiceRecording === 'function') {
            toggleVoiceRecording();
        }
    });

    // Send Button Click
    sendBtn.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            processUserInput(message);
            messageInput.value = '';
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
    .then(response => response.json())
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
            addMessageToChat('Error: ' + (data.error || 'Unknown error'), 'assistant-message');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('Communication error. Please try again.', 'assistant-message');
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
