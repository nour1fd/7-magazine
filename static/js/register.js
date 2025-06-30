// Password visibility toggle
document.getElementById('togglePassword1').addEventListener('click', function() {
    togglePasswordVisibility('id_password1', this);
});

document.getElementById('togglePassword2').addEventListener('click', function() {
    togglePasswordVisibility('id_password2', this);
});

function togglePasswordVisibility(inputId, icon) {
    const passwordInput = document.getElementById(inputId);
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    icon.textContent = type === 'password' ? '👁️' : '🔒';
}

// Image preview
document.getElementById('id_profile_image').addEventListener('change', function(e) {
    const preview = document.getElementById('previewImage');
    const previewText = document.querySelector('.image-preview-text');
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            previewText.style.display = 'none';
        }
        
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
        previewText.style.display = 'block';
    }
});

// Password strength meter
document.getElementById('id_password1').addEventListener('input', function() {
    const password = this.value;
    const strengthBar = document.getElementById('password-strength-bar');
    let strength = 0;
    
    // Check password length
    if (password.length >= 8) strength += 25;
    
    // Check for mixed case
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 25;
    
    // Check for numbers
    if (password.match(/([0-9])/)) strength += 25;
    
    // Check for special characters
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 25;
    
    strengthBar.style.width = strength + '%';
    
    // Update color based on strength
    if (strength < 50) {
        strengthBar.style.background = '#e63946';
    } else if (strength < 75) {
        strengthBar.style.background = '#f4a261';
    } else {
        strengthBar.style.background = '#2a9d8f';
    }
});

// Form validation
document.querySelector('form').addEventListener('submit', function(e) {
    const password1 = document.getElementById('id_password1').value;
    const password2 = document.getElementById('id_password2').value;
    
    if (password1 !== password2) {
        alert("Passwords don't match!");
        e.preventDefault();
    }
});
