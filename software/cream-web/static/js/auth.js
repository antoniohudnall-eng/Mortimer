// CREAM Auth JavaScript

const API_BASE = '/api';

// Toast notification
function showToast(message, type = '') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast ' + type;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Login handler
async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('.btn-primary');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    
    // Show loading
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    btn.disabled = true;
    
    const data = {
        email: form.email.value,
        password: form.password.value
    };
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast('Welcome back, ' + result.user.name.split(' ')[0] + '!', 'success');
            
            // Redirect to app
            setTimeout(() => {
                window.location.href = '/app';
            }, 500);
        } else {
            const error = await response.json();
            showToast(error.detail || 'Login failed', 'error');
        }
    } catch (err) {
        showToast('Network error. Please try again.', 'error');
    } finally {
        // Reset button
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        btn.disabled = false;
    }
}

// Register handler
async function handleRegister(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('.btn-primary');
    
    btn.disabled = true;
    btn.textContent = 'Creating account...';
    
    const data = {
        email: form.email.value,
        password: form.password.value,
        name: form.name.value,
        company: form.company.value
    };
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast('Welcome to CREAM, ' + result.user.name + '!', 'success');
            
            setTimeout(() => {
                window.location.href = '/app';
            }, 500);
        } else {
            const error = await response.json();
            showToast(error.detail || 'Registration failed', 'error');
        }
    } catch (err) {
        showToast('Network error. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Create Account';
    }
}

// Show register modal
function showRegister() {
    document.getElementById('register-modal').style.display = 'flex';
}

// Close register modal
function closeRegister() {
    document.getElementById('register-modal').style.display = 'none';
}

// Show forgot password (placeholder)
function showForgot() {
    showToast('Password reset coming soon', 'success');
}

// Check if already logged in
async function checkSession() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        if (response.ok) {
            // Already logged in, redirect to app
            window.location.href = '/app';
        }
    } catch (err) {
        // Not logged in, stay on login page
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check session on load
    checkSession();
    
    // Auto-fill demo credentials for development
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    if (emailInput && window.location.hostname === 'localhost') {
        // Don't auto-fill in production
    }
});
