document.getElementById('ticket__send__image__input').addEventListener('change', function() {
    if (this.files.length > 0) {
        document.getElementById('ticket__send__image__form').dispatchEvent(new Event('submit'));
    }
});

document.getElementById('ticket__send__image__form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('ticket__send__image__input');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    if (!file.type.match('image.*')) {
        alert('Please select an image file');
        fileInput.value = '';
        return;
    }
    
    const formData = new FormData();
    formData.append('ticket_id', ticketId);
    formData.append('file', file);
    
    fetch('/upload-file', {
        method: 'POST',
        body: formData,
        credentials: 'include'  // Важно: передаем куки и сессию
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            socket.emit('send_image', {
                ticket_id: ticketId,
                image_path: data.file_path
            });
            fileInput.value = '';
        } else {
            alert('Error: ' + data.error);
            fileInput.value = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading image');
        fileInput.value = '';
    });
});

document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const messageInput = this.querySelector('input[name="message_text"]');
    const message = messageInput.value.trim();
    
    if (message) {
        socket.emit('send_message', {
            ticket_id: ticketId,
            message: message
        });
        messageInput.value = '';
    }
});

function smoothScrollToBottom() {
    const messagesContainer = document.querySelector('.chat__messages');
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
}

window.addEventListener('DOMContentLoaded', smoothScrollToBottom);
window.addEventListener('load', smoothScrollToBottom);
window.addEventListener('resize', smoothScrollToBottom);