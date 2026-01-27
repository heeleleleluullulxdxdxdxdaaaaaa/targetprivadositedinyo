document.getElementById('profile__avatar__container__input').addEventListener('change', function() {
    if (this.files.length > 0) {
        document.getElementById('profile__avatar__container__form').submit();
    }
});

function previewImage(input, img_id) {
    const img = document.getElementById(img_id);
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            img.src = e.target.result;
            img.style.display = 'block';
        }
        
        reader.onerror = function() {
            console.error('Ошибка загрузки файла');
            img.style.display = 'none';
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}