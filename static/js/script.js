
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.redirect-button').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const href = this.getAttribute('href');
            window.location.href = href;
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {    
    document.querySelectorAll('.flash-message').forEach(message => {
        setTimeout(() => {
            message.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
});