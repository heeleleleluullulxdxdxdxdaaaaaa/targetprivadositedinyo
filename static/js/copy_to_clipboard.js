function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
        alert('Link was copied!');
        })
        .catch(err => {
        console.error('Error: ', err);

        copyToClipboardFallback(text);
        });
}

function copyToClipboardFallback(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        document.execCommand('copy');
        alert('Link was copied!');
    } catch (err) {
        alert('Error');
    }
    
    document.body.removeChild(textArea);
}