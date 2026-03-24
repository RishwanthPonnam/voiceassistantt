// Command handling with WhatsApp state management
let whatsappMode = false;

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
        showSystemMessage('👋 Welcome! Try: "open whatsapp message John hello" or "what time is it?"');
    }, 500);
});

function processUserInput(message) {
    // Display user message
    addMessageToChat(message, 'user-message');

    // Check if in WhatsApp mode
    if (whatsappMode && (message.toLowerCase().includes('message') || message.toLowerCase().includes('send'))) {
        handleWhatsAppMessage(message);
        return;
    }

    // Check if opening WhatsApp
    if (message.toLowerCase().includes('open whatsapp')) {
        handleOpenWhatsApp(message);
        return;
    }

    // Default command processing
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
        addMessageToChat('❌ Communication error. Please check localhost:5000', 'assistant-message');
    });
}

function handleOpenWhatsApp(message) {
    addMessageToChat('📱 Opening WhatsApp...', 'assistant-message');
    
    fetch('/api/voice/whatsapp/open', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addMessageToChat('✅ WhatsApp is opened!', 'assistant-message');
        addMessageToChat('📋 What would you like to do? Say: "message [contact] [your message]"', 'assistant-message');
        
        if (typeof speakText === 'function') {
            speakText('WhatsApp is opened. Please tell me who you want to message and what to say.');
        }
        
        whatsappMode = true;
        
        // Check if command also contains message details
        if (message.toLowerCase().includes('message') || message.toLowerCase().includes('send')) {
            const taskPart = message.replace(/open\s+whatsapp/i, '').trim();
            if (taskPart) {
                setTimeout(() => {
                    handleWhatsAppMessage(taskPart);
                }, 2000);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('❌ Could not open WhatsApp. Error: ' + error.message, 'assistant-message');
    });
}

function handleWhatsAppMessage(message) {
    // Parse contact and message from command
    // Pattern: "message [contact] [message]" or "[contact] [message]"
    
    let contact, messageText;
    
    // Try to match "message to [contact] [message]"
    let match = message.match(/message\s+to\s+(.+?)\s+(.+)/i);
    if (match) {
        contact = match[1].trim();
        messageText = match[2].trim();
    }
    
    // Try to match "send [message] to [contact]"
    if (!contact) {
        match = message.match(/send\s+(.+?)\s+to\s+(.+)/i);
        if (match) {
            messageText = match[1].trim();
            contact = match[2].trim();
        }
    }
    
    // Try to match "[contact] [message]"
    if (!contact) {
        match = message.match(/^([A-Za-z\s]+)\s+(.+)$/);
        if (match) {
            contact = match[1].trim();
            messageText = match[2].trim();
        }
    }
    
    if (!contact || !messageText) {
        addMessageToChat('⚠️ Please specify: "message [contact name] [your message]"', 'assistant-message');
        return;
    }
    
    addMessageToChat(`📤 Sending message to ${contact}...`, 'assistant-message');
    
    fetch('/api/voice/whatsapp/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            contact: contact,
            message: messageText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addMessageToChat(`✅ Message sent to ${data.contact}: "${messageText}"`, 'assistant-message');
            if (typeof speakText === 'function') {
                speakText(`Message sent to ${contact}`);
            }
            whatsappMode = false;
        } else {
            addMessageToChat('⚠️ ' + data.message, 'assistant-message');
        }
        
        if (typeof saveMessage === 'function') {
            saveMessage(message, data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('❌ Error sending message: ' + error.message, 'assistant-message');
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
