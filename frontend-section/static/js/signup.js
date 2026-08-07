// ========================================
// SIGNUP FORM
// ========================================

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('signupForm');

    const steps = document.querySelectorAll('.signup__step');

    const prevBtn = document.getElementById('prevStep');

    const nextBtn = document.getElementById('nextStep');

    const submitBtn = document.getElementById('submitStep');

    const stepIndicator = document.getElementById('currentStep');

    const messageBox = document.getElementById('formMessage');


    let currentStep = 1;

    const totalSteps = steps.length;


    // ========================================
    // Show Message
    // ========================================

    function showMessage(text, type = 'success') {

        messageBox.textContent = text;

        messageBox.className = 'signup__message';

        messageBox.classList.add(
            `signup__message--${type}`
        );

        messageBox.style.display = 'block';


        clearTimeout(window.messageTimeout);


        window.messageTimeout = setTimeout(() => {

            messageBox.style.display = 'none';

        }, 5000);
    }


    // ========================================
    // Update Step
    // ========================================

    function updateStep(step) {

        steps.forEach((el, index) => {

            el.classList.toggle(
                'signup__step--active',
                index === step - 1
            );

        });


        stepIndicator.textContent = step;


        // Previous button

        prevBtn.disabled = step === 1;


        // Last step

        if (step === totalSteps) {

            nextBtn.style.display = 'none';

            submitBtn.style.display = 'inline-flex';

        } else {

            nextBtn.style.display = 'inline-flex';

            submitBtn.style.display = 'none';
        }


        // Scroll to top on mobile

        const card = document.querySelector(
            '.signup__card'
        );


        if (
            window.innerWidth < 768 &&
            card
        ) {

            card.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }


    // ========================================
    // Next Step
    // ========================================

    function nextStep() {

        if (!validateStep(currentStep)) {
            return;
        }


        if (currentStep < totalSteps) {

            currentStep++;

            updateStep(currentStep);
        }
    }


    // ========================================
    // Previous Step
    // ========================================

    function prevStep() {

        if (currentStep > 1) {

            currentStep--;

            updateStep(currentStep);
        }
    }


    // ========================================
    // Validate Step
    // ========================================

    function validateStep(step) {

        const currentStepEl =
            document.querySelector(
                `.signup__step[data-step="${step}"]`
            );


        if (!currentStepEl) {
            return true;
        }


        const inputs =
            currentStepEl.querySelectorAll(
                'input[required], select[required], textarea[required]'
            );


        let isValid = true;


        // Remove old errors

        inputs.forEach(input => {

            input.classList.remove('error');

        });


        // Required fields

        inputs.forEach(input => {

            if (!input.value.trim()) {

                input.classList.add('error');

                isValid = false;
            }
        });


        // Password validation

        if (step === 1) {

            const password =
                document.getElementById('password');

            const confirm =
                document.getElementById('confirmPassword');


            if (
                password &&
                confirm &&
                password.value &&
                confirm.value &&
                password.value !== confirm.value
            ) {

                confirm.classList.add('error');

                showMessage(
                    'Passwords do not match!',
                    'error'
                );

                isValid = false;
            }


            if (
                password &&
                password.value &&
                password.value.length < 6
            ) {

                password.classList.add('error');

                showMessage(
                    'Password must be at least 6 characters!',
                    'error'
                );

                isValid = false;
            }
        }


        if (!isValid) {

            showMessage(
                'Please fill in all required fields.',
                'error'
            );
        }


        return isValid;
    }


    // ========================================
    // Submit Form
    // ========================================

    async function submitForm(e) {

        e.preventDefault();


        // ------------------------------------
        // Validate all steps
        // ------------------------------------

        let allValid = true;


        for (
            let i = 1;
            i <= totalSteps;
            i++
        ) {

            if (!validateStep(i)) {

                allValid = false;

                currentStep = i;

                updateStep(i);

                break;
            }
        }


        if (!allValid) {
            return;
        }


        // ------------------------------------
        // Collect form data
        // ------------------------------------

        const formData = {

            username:
                document.getElementById('username').value.trim(),

            email:
                document.getElementById('email').value.trim(),

            password:
                document.getElementById('password').value,

            password2:
                document.getElementById('confirmPassword').value,

            fullName:
                document.getElementById('fullName').value.trim(),

            age:
                document.getElementById('age').value,

            gender:
                document.getElementById('gender').value,

            city:
                document.getElementById('city').value || null,

            bio:
                document.getElementById('bio').value.trim()
        };


        // ------------------------------------
        // Disable button
        // ------------------------------------

        submitBtn.disabled = true;

        submitBtn.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Creating...';


        try {

            // --------------------------------
            // Send API request
            // --------------------------------

            const response = await fetch(
                '/api/signup/',
                {
                    method: 'POST',

                    headers: {
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify(formData)
                }
            );


            // --------------------------------
            // Parse JSON
            // --------------------------------

            let data;


            try {

                data = await response.json();

            } catch (error) {

                throw new Error(
                    'Server returned an invalid response.'
                );
            }


            // --------------------------------
            // Success
            // --------------------------------

            if (response.ok) {

                showMessage(
                    '✅ Account created successfully!',
                    'success'
                );


                // Save JWT

                if (
                    data.data &&
                    data.data.access &&
                    data.data.refresh
                ) {

                    localStorage.setItem(
                        'access_token',
                        data.data.access
                    );

                    localStorage.setItem(
                        'refresh_token',
                        data.data.refresh
                    );
                }


                // --------------------------------
                // Backend decides destination
                // --------------------------------

                if (data.redirect) {

                    setTimeout(() => {

                        window.location.href =
                            data.redirect;

                    }, 1000);

                } else {

                    showMessage(
                        'Account created, but redirect URL was not provided.',
                        'error'
                    );
                }


                return;
            }


            // --------------------------------
            // API validation error
            // --------------------------------

            showMessage(
                data.message ||
                'Something went wrong!',
                'error'
            );


            // Highlight fields

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

            console.error(
                'Signup error:',
                error
            );


            showMessage(
                'Unable to connect to the server.',
                'error'
            );


        } finally {

            submitBtn.disabled = false;

            submitBtn.innerHTML =
                'Create Account <i class="fas fa-check"></i>';
        }
    }


    // ========================================
    // Event Listeners
    // ========================================

    nextBtn.addEventListener(
        'click',
        nextStep
    );


    prevBtn.addEventListener(
        'click',
        prevStep
    );


    form.addEventListener(
        'submit',
        submitForm
    );


    // ========================================
    // Enter Key
    // ========================================

    document
        .querySelectorAll(
            '.signup__step input, .signup__step select'
        )
        .forEach(input => {

            input.addEventListener(
                'keydown',
                function (e) {

                    if (e.key !== 'Enter') {
                        return;
                    }


                    e.preventDefault();


                    if (
                        currentStep === totalSteps
                    ) {

                        form.dispatchEvent(
                            new Event('submit')
                        );

                    } else {

                        nextStep();
                    }
                }
            );
        });


    // ========================================
    // Password Match - Real Time
    // ========================================

    const confirmPassword =
        document.getElementById(
            'confirmPassword'
        );


    if (confirmPassword) {

        confirmPassword.addEventListener(
            'input',
            function () {

                const password =
                    document.getElementById(
                        'password'
                    );


                if (
                    this.value &&
                    password.value &&
                    this.value !== password.value
                ) {

                    this.classList.add('error');

                } else {

                    this.classList.remove('error');
                }
            }
        );
    }


    // ========================================
    // Initialize
    // ========================================

    updateStep(1);

});