// ========================================
// SIGNUP FORM — STEP NAVIGATION ONLY
// ========================================
// This form now submits normally to Django (method="post" in the HTML).
// This script ONLY handles the multi-step UI (showing/hiding steps,
// Next/Back buttons, client-side "did you fill this in" checks).
// It does NOT intercept the final submit or talk to any API —
// Django's view handles validation, errors, and redirecting.

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('signupForm');

    const steps = document.querySelectorAll('.signup__step');

    const prevBtn = document.getElementById('prevStep');

    const nextBtn = document.getElementById('nextStep');

    const submitBtn = document.getElementById('submitStep');

    const stepIndicator = document.getElementById('currentStep');


    let currentStep = 1;

    const totalSteps = steps.length;


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
    // Validate Step (client-side UX only)
    // ========================================
    // Django re-validates everything server-side regardless — this just
    // gives the user a fast in-browser hint instead of a round trip,
    // and stops empty hidden-step fields from slipping through (browsers
    // skip "required" checks on fields that are display:none).

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


        // Remove old error highlighting

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


        // Password match / length (step 1 only)

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

                isValid = false;
            }


            if (
                password &&
                password.value &&
                password.value.length < 6
            ) {

                password.classList.add('error');

                isValid = false;
            }
        }


        return isValid;
    }


    // ========================================
    // Final Submit Check
    // ========================================
    // Runs right before the browser sends the form to Django. If any
    // step is incomplete, we stop the submit and jump the user to the
    // first problem step. Otherwise we let the native form submission
    // proceed as normal — no preventDefault, no fetch.

    function onSubmit(e) {

        for (
            let i = 1;
            i <= totalSteps;
            i++
        ) {

            if (!validateStep(i)) {

                e.preventDefault();

                currentStep = i;

                updateStep(i);

                return;
            }
        }

        // All steps valid — let the form submit normally to Django.
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
        onSubmit
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


                    // On the last step, let Enter submit normally.

                    if (currentStep === totalSteps) {
                        return;
                    }


                    e.preventDefault();

                    nextStep();
                }
            );
        });


    // ========================================
    // Password Match — Real Time
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