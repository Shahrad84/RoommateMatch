// ========================================
// LOGIN FORM — UX ENHANCEMENTS ONLY
// ========================================
// This form submits natively to Django (method="post" in the HTML).
// This script does NOT intercept submission, call fetch, or touch
// the network in any way — it only adds small visual niceties.
// Safe to remove entirely; the form works without it.

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('loginForm');

    const loginBtn = document.getElementById('loginBtn');

    const usernameInput = document.getElementById('username');

    const passwordInput = document.getElementById('password');


    // ========================================
    // Clear error styling as user retypes
    // ========================================

    [usernameInput, passwordInput].forEach(input => {

        if (!input) {
            return;
        }

        input.addEventListener('input', function () {

            this.classList.remove('error');

        });

    });


    // ========================================
    // Password visibility toggle
    // ========================================
    // Only runs if a toggle button with this id exists in the HTML.
    // Safe no-op otherwise — nothing to add to the markup unless you want it.

    const toggleBtn = document.getElementById('togglePassword');

    if (toggleBtn && passwordInput) {

        toggleBtn.addEventListener('click', function () {

            const isHidden = passwordInput.type === 'password';

            passwordInput.type = isHidden ? 'text' : 'password';

            this.classList.toggle('fa-eye');

            this.classList.toggle('fa-eye-slash');

        });

    }


    // ========================================
    // Loading state on submit
    // ========================================
    // The browser is already navigating away by the time this runs,
    // so this only affects the brief moment before the page changes —
    // purely cosmetic, doesn't block or delay the actual submission.

    if (form && loginBtn) {

        form.addEventListener('submit', function () {

            loginBtn.disabled = true;

            loginBtn.innerHTML =
                '<i class="fas fa-spinner fa-spin"></i> Logging in...';

        });

    }

});