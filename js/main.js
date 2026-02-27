/* ============================================
   SHEGER INTERNATIONAL LLC
   Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // --- Mobile Navigation ---
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    let overlay = document.createElement('div');
    overlay.className = 'nav-overlay';
    document.body.appendChild(overlay);

    function openMenu() {
        navMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        navMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (navToggle) {
        navToggle.addEventListener('click', function () {
            if (navMenu.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }

    overlay.addEventListener('click', closeMenu);

    // Close menu on nav link click (mobile)
    document.querySelectorAll('.nav-menu a').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    // --- Sticky Navbar Shadow ---
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // --- Scroll Animations ---
    const fadeElements = document.querySelectorAll('.section-header, .vehicle-card, .service-card, .team-card, .market-card, .approach-card, .why-item, .intro-content, .intro-image, .about-content, .about-sidebar, .service-detail, .vision-item, .contact-form, .contact-info-card');

    fadeElements.forEach(function (el) {
        el.classList.add('fade-in');
    });

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    fadeElements.forEach(function (el) {
        observer.observe(el);
    });

    // --- Inventory Filter ---
    const filterBtns = document.querySelectorAll('.filter-btn');
    const vehicleCards = document.querySelectorAll('.vehicle-card[data-category]');

    filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            // Update active button
            filterBtns.forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            vehicleCards.forEach(function (card) {
                if (filter === 'all') {
                    card.style.display = '';
                    setTimeout(function () { card.classList.add('visible'); }, 50);
                } else {
                    const categories = card.getAttribute('data-category');
                    if (categories && categories.includes(filter)) {
                        card.style.display = '';
                        setTimeout(function () { card.classList.add('visible'); }, 50);
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });

    // --- Contact Form Handling ---
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            // Basic validation visual feedback
            const requiredFields = contactForm.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(function (field) {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) return;

            // Simulate submission
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            setTimeout(function () {
                submitBtn.textContent = 'Inquiry Submitted!';
                submitBtn.style.background = '#25d366';

                // Reset after delay
                setTimeout(function () {
                    contactForm.reset();
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }, 1500);
        });

        // Remove error styling on input
        contactForm.querySelectorAll('input, select, textarea').forEach(function (field) {
            field.addEventListener('input', function () {
                field.style.borderColor = '';
            });
        });
    }

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});
