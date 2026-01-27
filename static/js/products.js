document.addEventListener('DOMContentLoaded', function() {
    const imageContainers = document.querySelectorAll('.products__item__image__container');
    
    imageContainers.forEach(container => {
        const images = container.querySelectorAll('.product-image');
        const indicators = container.closest('.products__item')
                                .querySelectorAll('.products__item__image__state');
        
        // Показываем переключение только если есть минимум 2 изображения
        if (images.length < 2) return;
        
        container.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const width = rect.width;
            const percentage = (x / width) * 100;
            
            // Определяем количество сегментов в зависимости от количества изображений
            const segmentCount = images.length;
            const segmentSize = 100 / segmentCount;
            
            let activeImageIndex = 1;
            
            // Определяем активное изображение на основе позиции курсора
            for (let i = 0; i < segmentCount; i++) {
                if (percentage <= (i + 1) * segmentSize) {
                    activeImageIndex = i + 1;
                    break;
                }
            }
            
            // Активируем соответствующее изображение
            images.forEach(img => {
                const imageIndex = parseInt(img.dataset.image);
                if (imageIndex === activeImageIndex) {
                    img.classList.add('active');
                    img.style.display = 'block';
                } else {
                    img.classList.remove('active');
                    img.style.display = 'none';
                }
            });
            
            // Обновляем индикаторы
            indicators.forEach(indicator => {
                const stateIndex = parseInt(indicator.dataset.state);
                indicator.classList.toggle('active', stateIndex === activeImageIndex);
            });
        });
        
        // Возвращаем первое изображение когда курсор уходит
        container.addEventListener('mouseleave', function() {
            images.forEach((img, index) => {
                if (index === 0) {
                    img.classList.add('active');
                    img.style.display = 'block';
                } else {
                    img.classList.remove('active');
                    img.style.display = 'none';
                }
            });
            
            // Сбрасываем индикаторы на первый
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === 0);
            });
        });
    });
});