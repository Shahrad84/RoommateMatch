// ========================================
// DASHBOARD - INTERACTIVE FEATURES
// ========================================

document.addEventListener('DOMContentLoaded', function () {

    // ========================================
    // ANIMATE PROGRESS BAR ON LOAD
    // ========================================
    
    const progressBar = document.querySelector('.profile-progress__bar');
    
    if (progressBar) {
        // Reset width to 0 then animate to target
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0%';
        
        setTimeout(() => {
            progressBar.style.transition = 'width 1s ease-in-out';
            progressBar.style.width = targetWidth;
        }, 300);
    }


    // ========================================
    // CONFIRMATION FOR COMPLETE PROFILE BUTTON
    // ========================================
    
    const completeProfileBtn = document.querySelector('.profile-completion--incomplete .btn--primary');
    
    if (completeProfileBtn) {
        completeProfileBtn.addEventListener('click', function(e) {
            // Optional: Add a loading state
            this.innerHTML = 'Loading... <i class="fas fa-spinner fa-spin"></i>';
            
            // Let the link work normally (no preventDefault)
        });
    }


    // ========================================
    // TOOLTIP FOR LOCKED FEATURES
    // ========================================
    
    const lockedFeatures = document.querySelectorAll('.dashboard-feature--locked');
    
    lockedFeatures.forEach(feature => {
        feature.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show a message when clicking locked features
            alert('⚠️ Please complete your profile first to unlock this feature.');
            
            // Or highlight the complete profile button
            const completeBtn = document.querySelector('.profile-completion--incomplete .btn--primary');
            if (completeBtn) {
                completeBtn.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    completeBtn.style.transform = 'scale(1)';
                }, 200);
            }
        });
    });


    // ========================================
    // GREETING BASED ON TIME OF DAY
    // ========================================
    
    const greetingElement = document.querySelector('.dashboard__subtitle');
    
    if (greetingElement) {
        const hour = new Date().getHours();
        let greeting;
        
        if (hour < 12) {
            greeting = 'Good morning';
        } else if (hour < 18) {
            greeting = 'Good afternoon';
        } else {
            greeting = 'Good evening';
        }
        
        // Update subtitle with time-based greeting
        const username = document.querySelector('.dashboard__title');
        if (username) {
            const userName = username.textContent.replace('Welcome, ', '').replace(' 👋', '');
            greetingElement.textContent = `${greeting}, ${userName}! Find a roommate who matches your lifestyle.`;
        }
    }


    // ========================================
    // SMOOTH SCROLL FOR FEATURE CARDS
    // ========================================
    
    const featureCards = document.querySelectorAll('.dashboard-feature:not(.dashboard-feature--locked)');
    
    featureCards.forEach((card, index) => {
        // Add subtle entrance animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.5s ease ${index * 0.1}s`;
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });

});