function formatDescText(element) {
    // Сохраняем оригинальные стили
    const originalStyles = window.getComputedStyle(element);
    const lineHeight = originalStyles.lineHeight;
    const fontSize = originalStyles.fontSize;
    const fontFamily = originalStyles.fontFamily;
    const color = originalStyles.color;
    
    let text = element.textContent;
    
    // Обработка ссылок в формате [текст](url)
    const linkPattern = /\[([^\]]+)\]\(([^)]+)\)/g;
    text = text.replace(linkPattern, 
        '<a href="$2" style="color: var(--accent); text-decoration: underline;">$1</a>'
    );
    
    // Обработка строк с тире в начале - преобразование в список
    const lines = text.split('\n');
    let inList = false;
    let formattedLines = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // Если строка начинается с тире (учитываем возможные пробелы перед тире)
        if (line.trim().startsWith('-')) {
            if (!inList) {
                // Начало нового списка
                formattedLines.push(`<ul style="padding-left: 20px; line-height: ${lineHeight}; font-size: ${fontSize}; font-family: ${fontFamily}; color: ${color};">`);
                inList = true;
            }
            // Заменяем тире на bullet point и добавляем как элемент списка
            const listItem = line.replace('-', '').trim();
            formattedLines.push(`<li style="line-height: ${lineHeight};">${listItem}</li>`);
        } else {
            if (inList) {
                // Завершаем предыдущий список
                formattedLines.push('</ul>');
                inList = false;
            }
            // Добавляем обычную строку
            if (line.trim() === '') {
                // Пустые строки - добавляем параграф для отступа
                formattedLines.push(`<p style="margin: 5px 0; line-height: ${lineHeight}; font-size: ${fontSize}; font-family: ${fontFamily}; color: ${color};"></p>`);
            } else {
                formattedLines.push(`<p style="margin: 10px 0; line-height: ${lineHeight}; font-size: ${fontSize}; font-family: ${fontFamily}; color: ${color};">${line}</p>`);
            }
        }
    }
    
    // Если текст заканчивается списком, закрываем его
    if (inList) {
        formattedLines.push('</ul>');
    }
    
    element.innerHTML = formattedLines.join('');
}

const productDesc = document.getElementById('product_desc');
if (productDesc) {
    formatDescText(productDesc);
}