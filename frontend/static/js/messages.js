// Message storage and retrieval
function saveMessage(userMessage, assistantResponse) {
    fetch('/api/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_message: userMessage,
            assistant_response: assistantResponse
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            console.log('Message saved with ID:', data.id);
        }
    })
    .catch(error => console.error('Error saving message:', error));
}

function loadMessageHistory() {
    fetch('/api/messages/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(messages => {
        console.log('Loaded messages:', messages);
        // Optionally display message history
        if (messages.length === 0) {
            console.log('No previous messages found');
        }
    })
    .catch(error => console.error('Error loading messages:', error));
}

function deleteMessage(messageId) {
    fetch(`/api/messages/${messageId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Message deleted:', data.message);
    })
    .catch(error => console.error('Error deleting message:', error));
}

// Load message history on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMessageHistory();
});
