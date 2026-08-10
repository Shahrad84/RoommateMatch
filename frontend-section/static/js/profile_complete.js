// ========================================
// PROFILE COMPLETE - MULTI STEP FORM
// ========================================

document.addEventListener('DOMContentLoaded', function () {

const form = document.getElementById('profileForm');
const steps = document.querySelectorAll('.profile-step');
const messageBox = document.getElementById('formMessage');

let currentStep = 1;
const totalSteps = steps.length;


// ========================================
// UPDATE STEP
// ========================================

function updateStep(step) {

    steps.forEach((element, index) => {

        element.classList.toggle(
            'profile-step--active',
            index === step - 1
        );

    });


    // Update progress indicator

    document.querySelectorAll('.progress-step').forEach((element, index) => {

        element.classList.toggle(
            'progress-step--active',
            index < step
        );

    });

}


// ========================================
// SHOW MESSAGE
// ========================================

function showMessage(text, type = 'success') {

    if (!messageBox) {
        return;
    }

    messageBox.textContent = text;

    messageBox.className = 'form-message';

    messageBox.classList.add(
        `form-message--${type}`
    );

    messageBox.style.display = 'block';


    clearTimeout(window.profileMessageTimeout);

    window.profileMessageTimeout = setTimeout(() => {

        messageBox.style.display = 'none';

    }, 5000);

}


// ========================================
// VALIDATE STEP
// ========================================

function validateStep(step) {

    const currentStepElement =
        document.querySelector(
            `.profile-step[data-step="${step}"]`
        );


    if (!currentStepElement) {
        return false;
    }


    const inputs =
        currentStepElement.querySelectorAll(
            'input[required], select[required], textarea[required]'
        );


    let isValid = true;


    inputs.forEach(input => {

        input.classList.remove('error');


        // Checkbox / radio

        if (
            input.type === 'checkbox' ||
            input.type === 'radio'
        ) {

            const group =
                currentStepElement.querySelectorAll(
                    `input[name="${input.name}"]`
                );


            const checked =
                Array.from(group).some(
                    item => item.checked
                );


            if (!checked) {

                input.classList.add('error');

                isValid = false;

            }

            return;
        }


        // Normal inputs

        if (!input.value.trim()) {

            input.classList.add('error');

            isValid = false;

        }

    });


    if (!isValid) {

        showMessage(
            'Please fill in all required fields.',
            'error'
        );

    }


    return isValid;
}


// ========================================
// NEXT STEP
// ========================================

function nextStep() {

    // Current step must be valid

    if (!validateStep(currentStep)) {
        return;
    }


    if (currentStep < totalSteps) {

        currentStep++;

        updateStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

    }

}


// ========================================
// PREVIOUS STEP
// ========================================

function previousStep() {

    if (currentStep > 1) {

        currentStep--;

        updateStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

    }

}


// ========================================
// SUBMIT FORM
// ========================================

async function submitForm(event) {

    event.preventDefault();


    // Validate current step

    if (!validateStep(currentStep)) {
        return;
    }


    // Validate all previous steps as well

    for (let step = 1; step <= totalSteps; step++) {

        if (!validateStep(step)) {

            currentStep = step;

            updateStep(currentStep);

            return;
        }

    }


    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );


    if (submitButton) {

        submitButton.disabled = true;

        submitButton.innerHTML =
            'Saving...';

    }


    /*
     * FormData contains all inputs from
     * all three steps.
     *
     * Django will receive them through:
     *
     * request.POST
     */

    const formData = new FormData(form);


    try {

        const response = await fetch(
            '/profile/complete/',
            {
                method: 'POST',

                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },

                body: formData
            }
        );


        const data = await response.json();


        if (response.ok && data.success) {

            showMessage(
                'Profile completed successfully!',
                'success'
            );


            /*
             * Backend can return the destination.
             *
             * Example:
             *
             * {
             *     "success": true,
             *     "redirect_url": "/dashboard/"
             * }
             */

            const redirectUrl =
                data.redirect_url || '/dashboard/';


            setTimeout(() => {

                window.location.href =
                    redirectUrl;

            }, 1000);

        } else {

            showMessage(
                data.message ||
                'Something went wrong.',
                'error'
            );


            /*
             * Backend can return field errors:
             *
             * {
             *     "errors": {
             *         "job": "Job is required"
             *     }
             * }
             */

            if (data.errors) {

                Object.keys(data.errors).forEach(fieldName => {

                    const field =
                        form.querySelector(
                            `[name="${fieldName}"]`
                        );


                    if (field) {

                        field.classList.add('error');

                    }

                });

            }

        }

    } catch (error) {

        console.error(
            'Profile submission error:',
            error
        );


        showMessage(
            'Network error. Please try again.',
            'error'
        );

    } finally {

        if (submitButton) {

            submitButton.disabled = false;

            submitButton.innerHTML =
                'Complete Profile ✓';

        }

    }

}


// ========================================
// NEXT BUTTONS
// ========================================

document
    .querySelectorAll('[data-next]')
    .forEach(button => {

        button.addEventListener(
            'click',
            nextStep
        );

    });


// ========================================
// PREVIOUS BUTTONS
// ========================================

document
    .querySelectorAll('[data-prev]')
    .forEach(button => {

        button.addEventListener(
            'click',
            previousStep
        );

    });


// ========================================
// FORM SUBMIT
// ========================================

if (form) {

    form.addEventListener(
        'submit',
        submitForm
    );

}


// ========================================
// RANGE INPUTS
// ========================================

document
    .querySelectorAll('input[type="range"]')
    .forEach(range => {

        range.addEventListener(
            'input',
            function () {

                const valueElement =
                    document.getElementById(
                        this.id + 'Value'
                    );


                if (valueElement) {

                    valueElement.textContent =
                        this.value;

                }

            }
        );

    });


// ========================================
// ENTER KEY
// ========================================

document
    .querySelectorAll(
        '.profile-step input, .profile-step select, .profile-step textarea'
    )
    .forEach(input => {

        input.addEventListener(
            'keydown',
            function (event) {

                if (event.key !== 'Enter') {
                    return;
                }


                // Don't submit textarea with Enter

                if (this.tagName === 'TEXTAREA') {
                    return;
                }


                event.preventDefault();


                if (currentStep < totalSteps) {

                    nextStep();

                } else {

                    form.requestSubmit();

                }

            }
        );

    });


// ========================================
// INITIALIZE
// ========================================

if (totalSteps > 0) {

    updateStep(1);

}


});
