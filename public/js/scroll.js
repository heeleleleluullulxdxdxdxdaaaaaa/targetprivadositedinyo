function smoothScrollTo(elementId, options = {}) {
    const {
        offset = 75,
        duration = 800,
        containerSelector = '.root'
    } = options;
    
    const targetElement = document.getElementById(elementId);
    const container = document.querySelector(containerSelector);
    
    if (!targetElement) {
        // Ищем активный элемент (кнопку/ссылку, которая вызвала скролл)
        const activeElement = document.activeElement;
        if (activeElement && activeElement.hasAttribute('href')) {
            const href = activeElement.getAttribute('href');
            
            // Если href - это якорная ссылка (начинается с #)
            if (href && href.startsWith('#')) {
                const targetId = href.substring(1);
                const targetFromHref = document.getElementById(targetId);
                
                if (targetFromHref && container) {
                    // Рекурсивно вызываем функцию с ID из href
                    smoothScrollTo(targetId, options);
                    return;
                }
            }
            
            // Если это обычная ссылка (не якорь) или элемент всё равно не найден
            if (href && !href.startsWith('#')) {
                window.location.href = href;
                return;
            }
        }
        
        // Если не удалось найти элемент и нет подходящего href
        console.warn(`Element with ID "${elementId}" not found on the page`);
        return;
    }
    
    if (!container) {
        console.warn(`Container with selector "${containerSelector}" not found`);
        return;
    }
    
    const targetPosition = targetElement.offsetTop - container.offsetTop - offset;
    const startPosition = container.scrollTop;
    const distance = targetPosition - startPosition;
    let startTime = null;
    
    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = easeInOutQuad(timeElapsed, startPosition, distance, duration);
        container.scrollTop = run;
        
        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }
    
    function easeInOutQuad(t, b, c, d) {
        t /= d/2;
        if (t < 1) return c/2*t*t + b;
        t--;
        return -c/2 * (t*(t-2) - 1) + b;
    }
    
    requestAnimationFrame(animation);
}

function scrollToElement(elementId) {
    smoothScrollTo(elementId, {
        offset: 75,
        duration: 800,
        containerSelector: '.root'
    });
}