document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('loginForm');
    const messageBox = document.getElementById('loginMessage');
    const loginBtn = document.getElementById('loginBtn');

    // ==============================
    // Show Message
    // ==============================

    function showMessage(text, type = 'success') {

        messageBox.textContent = text;
        messageBox.className = 'login__message';
        messageBox.classList.add(`login__message--${type}`);
        messageBox.style.display = 'block';

        clearTimeout(window.messageTimeout);

        window.messageTimeout = setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }


    // ==============================
    // Submit Login
    // ==============================

    async function submitLogin(e) {

        e.preventDefault();

        // Clear previous errors
        document
            .querySelectorAll('.error')
            .forEach(el => el.classList.remove('error'));


        const username =
            document.getElementById('username').value.trim();

        const password =
            document.getElementById('password').value;


        // ==============================
        // Client-side validation
        // ==============================

        if (!username) {

            document
                .getElementById('username')
                .classList.add('error');

            showMessage(
                'Username is required',
                'error'
            );

            return;
        }


        if (!password) {

            document
                .getElementById('password')
                .classList.add('error');

            showMessage(
                'Password is required',
                'error'
            );

            return;
        }


        // ==============================
        // Disable button
        // ==============================

        loginBtn.disabled = true;

        loginBtn.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Logging in...';


        try {

            // ==============================
            // Send request
            // ==============================

            const response = await fetch('/api/login/', {

                method: 'POST',

                headers: {
                    'Content-Type': 'application/json',
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });


            // ==============================
            // Parse response
            // ==============================

            const data = await response.json();


            // ==============================
            // Successful login
            // ==============================

            if (response.ok) {

                // Save JWT
                localStorage.setItem(
                    'access_token',
                    data.data.access
                );

                localStorage.setItem(
                    'refresh_token',
                    data.data.refresh
                );


                showMessage(
                    'Login successful! Redirecting...',
                    'success'
                );


                // Backend determines destination
                setTimeout(() => {

                    window.location.href =
                        data.redirect;

                }, 800);


                return;
            }


            // ==============================
            // Backend validation error
            // ==============================

            showMessage(
                data.message || 'Login failed',
                'error'
            );


            // Highlight fields with errors
            if (data.errors) {

                Object.keys(data.errors).forEach(key => {

                    const field =
                        document.getElementById(key);

                    if (field) {
                        field.classList.add('error');
                    }
                });
            }


        } catch (error) {

            console.error('Login error:', error);

            showMessage(
                'Unable to connect to the server.',
                'error'
            );

        } finally {

            loginBtn.disabled = false;

            loginBtn.innerHTML =
                'Log In <i class="fas fa-arrow-right"></i>';
        }
    }


    // ==============================
    // Event Listener
    // ==============================

    form.addEventListener(
        'submit',
        submitLogin
    );

});