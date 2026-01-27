document.addEventListener('DOMContentLoaded', function() {
    const currentVersion = document.body.getAttribute('data-version');
    const savedVersion = localStorage.getItem('htmlVersion');

    if (savedVersion !== currentVersion) 
    {
        localStorage.setItem('htmlVersion', currentVersion);
        location.reload(true);
    }
});