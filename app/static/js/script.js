// Silence is Golden

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');
const confirm_password = document.querySelector('#confirm_password');

togglePassword.addEventListener('click', () => {
    togglePassword.classList.toggle('bi-eye');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    confirm_password.setAttribute('type', type);
})