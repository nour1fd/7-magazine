// Password visibility toggle
document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('id_password');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.textContent = type === 'password' ? '👁️' : '🔒';
});

// Auto focus on username field
document.getElementById('id_username').focus();

// Remember me functionality
document.addEventListener('DOMContentLoaded', function() {
    const rememberCheckbox = document.getElementById('remember_me');
    const usernameInput = document.getElementById('id_username');
    
    // Check if credentials exist in localStorage
    if (localStorage.getItem('remember_me') === 'true') {
        rememberCheckbox.checked = true;
        usernameInput.value = localStorage.getItem('username') || '';
    }
    
    // Save credentials when form is submitted
    document.querySelector('form').addEventListener('submit', function() {
        if (rememberCheckbox.checked) {
            localStorage.setItem('remember_me', 'true');
            localStorage.setItem('username', usernameInput.value);
        } else {
            localStorage.removeItem('remember_me');
            localStorage.removeItem('username');
        }
    });
});

// Form validation
document.querySelector('form').addEventListener('submit', function(e) {
    const username = document.getElementById('id_username').value.trim();
    const password = document.getElementById('id_password').value;
    
    if (!username) {
        alert("Please enter your username or email!");
        e.preventDefault();
        return;
    }
    
    if (!password) {
        alert("Please enter your password!");
        e.preventDefault();
        return;
    }
});