document.addEventListener('DOMContentLoaded', function() {

    const usernameInputElement = document.querySelector('.auth-wrapper__form-inner__input input[name="username"]');
    const usernameFormElement = document.querySelector('.auth-wrapper__form-inner__input.username');

    usernameInputElement.addEventListener('focus', () => {
        usernameFormElement.classList.add('active');
    });

    usernameInputElement.addEventListener('blur', () => {
        if (usernameInputElement.value.length === 0) {
            usernameFormElement.classList.remove('active');
        }
    });

    // Проверяем при загрузке страницы, если поле уже заполнено
    if (usernameInputElement.value.length > 0) {
        usernameFormElement.classList.add('active');
    }

    const passwordInputElement = document.querySelector('.auth-wrapper__form-inner__input input[name="password"]');
    const passwordFormElement = document.querySelector('.auth-wrapper__form-inner__input.password');

    passwordInputElement.addEventListener('focus', () => {
        passwordFormElement.classList.add('active');
    });

    passwordInputElement.addEventListener('blur', () => {
        if (passwordInputElement.value.length === 0) {
            passwordFormElement.classList.remove('active');
        }
    });

    // Проверяем при загрузке страницы, если поле уже заполнено
    if (passwordInputElement.value.length > 0) {
        passwordFormElement.classList.add('active');
    }
});