// frontend-section/static/js/signup.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const steps = document.querySelectorAll('.signup__step');
    const prevBtn = document.getElementById('prevStep');
    const nextBtn = document.getElementById('nextStep');
    const submitBtn = document.getElementById('submitStep');
    const stepIndicator = document.getElementById('currentStep');
    const messageBox = document.getElementById('formMessage');

    let currentStep = 1;
    const totalSteps = steps.length;

    // ====== Update Step ======
    function updateStep(step) {
        steps.forEach((el, index) => {
            el.classList.toggle('signup__step--active', index === step - 1);
        });

        stepIndicator.textContent = step;

        prevBtn.disabled = step === 1;
        
        if (step === totalSteps) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }

        // Scroll to top on mobile
        const card = document.querySelector('.signup__card');
        if (window.innerWidth < 768) {
            card.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // ====== Next Step ======
    function nextStep() {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps) {
                currentStep++;
                updateStep(currentStep);
            }
        }
    }

    // ====== Previous Step ======
    function prevStep() {
        if (currentStep > 1) {
            currentStep--;
            updateStep(currentStep);
        }
    }

    // ====== Validate Current Step ======
    function validateStep(step) {
        const currentStepEl = document.querySelector(`.signup__step[data-step="${step}"]`);
        const inputs = currentStepEl.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => input.classList.remove('error'));

        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('error');
                isValid = false;
            }
        });

        // Password match (step 1)
        if (step === 1) {
            const password = document.getElementById('password');
            const confirm = document.getElementById('confirmPassword');
            
            if (password.value && confirm.value && password.value !== confirm.value) {
                confirm.classList.add('error');
                showMessage('Passwords do not match!', 'error');
                isValid = false;
            }
            
            if (password.value && password.value.length < 6) {
                password.classList.add('error');
                showMessage('Password must be at least 6 characters!', 'error');
                isValid = false;
            }
        }

        if (!isValid) {
            showMessage('Please fill in all required fields.', 'error');
        }

        return isValid;
    }

    // ====== Show Message ======
    function showMessage(text, type = 'success') {
        messageBox.textContent = text;
        messageBox.className = 'signup__message';
        messageBox.classList.add(`signup__message--${type}`);
        messageBox.style.display = 'block';

        clearTimeout(window.messageTimeout);
        window.messageTimeout = setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }

    // ====== Submit Form ======
    async function submitForm(e) {
        e.preventDefault();

        let allValid = true;
        for (let i = 1; i <= totalSteps; i++) {
            if (!validateStep(i)) {
                allValid = false;
                currentStep = i;
                updateStep(i);
                break;
            }
        }

        if (!allValid) return;

        // ====== فقط اطلاعات اکانت و پایه ======
        const formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            password2: document.getElementById('confirmPassword').value,
            fullName: document.getElementById('fullName').value,
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            city: document.getElementById('city').value || null,
            bio: document.getElementById('bio').value || ''
        };

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';

        try {
            const response = await fetch('/api/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('✅ Account created successfully!', 'success');
                
                if (data.data?.access) {
                    localStorage.setItem('access_token', data.data.access);
                    localStorage.setItem('refresh_token', data.data.refresh);
                }

                setTimeout(() => {
                    window.location.href = '/accounts/login/';
                }, 2000);
            } else {
                showMessage(data.message || 'Something went wrong!', 'error');
                if (data.errors) {
                    Object.keys(data.errors).forEach(key => {
                        const field = document.getElementById(key);
                        if (field) field.classList.add('error');
                    });
                }
            }
        } catch (error) {
            showMessage('Network error. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Create Account <i class="fas fa-check"></i>';
        }
    }

    // ====== Event Listeners ======
    nextBtn.addEventListener('click', nextStep);
    prevBtn.addEventListener('click', prevStep);
    form.addEventListener('submit', submitForm);

    document.querySelectorAll('.signup__step input, .signup__step select').forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (currentStep === totalSteps) {
                    form.dispatchEvent(new Event('submit'));
                } else {
                    nextStep();
                }
            }
        });
    });

    // Password match real-time
    document.getElementById('confirmPassword')?.addEventListener('input', function() {
        const password = document.getElementById('password');
        if (this.value && password.value && this.value !== password.value) {
            this.classList.add('error');
        } else {
            this.classList.remove('error');
        }
    });

    // ====== Init ======
    updateStep(1);
});