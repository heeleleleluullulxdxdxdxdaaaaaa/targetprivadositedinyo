document.addEventListener('DOMContentLoaded', () => {
    // Select toggles
    const toggleBox = document.getElementById('toggle-box');
    const toggleHealth = document.getElementById('toggle-health');
    const toggleHead = document.getElementById('toggle-head');
    const toggleDistance = document.getElementById('toggle-distance');
    const toggleWeapon = document.getElementById('toggle-weapon');
    const toggleName = document.getElementById('toggle-name');

    // Select ESP groups
    const espBox = document.getElementById('esp-box');
    const espHealth = document.getElementById('esp-health');
    const espHead = document.getElementById('esp-head');
    const espDistance = document.getElementById('esp-distance');
    const espWeapon = document.getElementById('esp-weapon');
    const espName = document.getElementById('esp-name');

    // Function to handle toggle logic
    function setupToggle(toggleEl, targetGroup) {
        if (!toggleEl || !targetGroup) return;

        // Initial state
        if (toggleEl.checked) {
            targetGroup.classList.add('active');
        } else {
            targetGroup.classList.remove('active');
        }

        // Change event
        toggleEl.addEventListener('change', (e) => {
            if (e.target.checked) {
                targetGroup.classList.add('active');
                animateHighlight(targetGroup);
            } else {
                targetGroup.classList.remove('active');
            }
        });
    }

    // Initialize all ESP toggles
    setupToggle(toggleBox, espBox);
    setupToggle(toggleHealth, espHealth);
    setupToggle(toggleHead, espHead);
    setupToggle(toggleDistance, espDistance);
    setupToggle(toggleWeapon, espWeapon);
    setupToggle(toggleName, espName);

    // Color Pickers Logic
    const colorPickers = [
        { id: 'color-box', variable: '--color-box' },
        { id: 'color-head', variable: '--color-head' },
        { id: 'color-text', variable: '--color-text' }
    ];

    colorPickers.forEach(picker => {
        const input = document.getElementById(picker.id);
        if (input) {
            // Set initial color value if overriding default css
            document.documentElement.style.setProperty(picker.variable, input.value);

            // Listen for live color changes
            input.addEventListener('input', (e) => {
                document.documentElement.style.setProperty(picker.variable, e.target.value);
            });
        }
    });

    // Micro-animation for activating an element (brief bright flash)
    function animateHighlight(element) {
        if (!element) return;
        // Replaced scale transforms with pure CSS opacity transitions
        // to prevent Chrome/Edge from blurring SVG texts during hardware acceleration
        element.style.opacity = '0.5';
        setTimeout(() => {
            element.style.opacity = '';
        }, 150);
    }



    // Image Comparison Slider Logic
    const compInput = document.getElementById('comp-input');
    const compOverlay = document.getElementById('comp-overlay');
    const compHandle = document.getElementById('comp-handle');

    if (compInput && compOverlay && compHandle) {
        compInput.addEventListener('input', (e) => {
            const val = e.target.value;
            // Update the width to clip instead of using complex clip-path
            compOverlay.style.width = `${val}%`;
            // Counter-scale the image inside to keep it fixed in space
            const img = compOverlay.querySelector('img');
            if (img && val > 0) {
                img.style.width = `${(100 / val) * 100}%`;
            }
            compHandle.style.left = `${val}%`;
        });
    }

    // Video Modal Logic
    const openVideoBtn = document.getElementById('open-video-btn');
    const closeVideoBtn = document.getElementById('close-video-btn');
    const videoModal = document.getElementById('video-modal-overlay');
    const heroVideoIframe = document.getElementById('hero-video-iframe');

    // Make sure we embed the video URL sent by the user with autoplay
    const videoURL = "https://www.youtube.com/embed/CnxTOY2eheo?si=vD75jQHSwbJN_kU4&autoplay=1";

    if (openVideoBtn && closeVideoBtn && videoModal && heroVideoIframe) {
        // Open Modal
        openVideoBtn.addEventListener('click', () => {
            heroVideoIframe.src = videoURL; // Set src to trigger autoplay
            videoModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent page scrolling
        });

        // Close Modal
        closeVideoBtn.addEventListener('click', () => {
            videoModal.classList.remove('active');
            // Remove src after animation ends to stop audio/video
            setTimeout(() => {
                heroVideoIframe.src = "";
            }, 300);
            document.body.style.overflow = '';
        });

        // Close on outside click
        videoModal.addEventListener('click', (e) => {
            // Check if the click was directly on the overlay backdrop
            if (e.target.id === 'video-modal-overlay') {
                closeVideoBtn.click();
            }
        });
    }
    // --- How-To Section Interactive Slider Logic ---
    const howToItems = document.querySelectorAll('.how-to-item');
    const howToImage = document.getElementById('how-to-main-image');
    let howToIndex = 0;
    const collapseDelay = 3000; // 3 seconds - faster cycle
    let howToInterval;

    function updateHowTo(index) {
        // Reset all
        howToItems.forEach(item => {
            item.classList.remove('active');
        });

        // Set active
        const activeItem = howToItems[index];
        activeItem.classList.add('active');

        // Change current index
        howToIndex = index;
    }

    function startHowToAutoCycle() {
        if (howToInterval) clearInterval(howToInterval);

        // Initial run for first item
        updateHowTo(howToIndex);

        howToInterval = setInterval(() => {
            howToIndex = (howToIndex + 1) % howToItems.length;
            updateHowTo(howToIndex);
        }, collapseDelay);
    }

    if (howToItems.length > 0) {
        startHowToAutoCycle();
    }
    // --- BlurFade Reveal Logic (Strictly Once) ---
    const blurObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                if (!el.classList.contains('show')) {
                    const delay = parseFloat(el.getAttribute('data-delay') || 0) * 1000;
                    setTimeout(() => {
                        el.classList.add('show');
                    }, delay);
                    blurObserver.unobserve(el);
                }
            }
        });
    }, { threshold: 0.05, rootMargin: "0px" });

    // Apply to all blur-fade elements
    document.querySelectorAll('.blur-fade').forEach(el => {
        // If it's a hero element and near the top, trigger it faster
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            // Already in view on load
            const delay = parseFloat(el.getAttribute('data-delay') || 0) * 1000;
            setTimeout(() => {
                el.classList.add('show');
            }, delay);
        } else {
            blurObserver.observe(el);
        }
    });
    // Music Logic - Background Autoplay & Navbar Toggle
    const music = document.getElementById('bg-music');
    const navMusicToggle = document.getElementById('nav-music-toggle');
    const onIcon = document.querySelector('.music-on-icon');
    const offIcon = document.querySelector('.music-off-icon');

    if (music) {
        music.volume = 0.20;

        const updateMusicIcons = () => {
            if (music.paused) {
                if (onIcon) onIcon.style.display = 'none';
                if (offIcon) offIcon.style.display = 'block';
            } else {
                if (onIcon) onIcon.style.display = 'block';
                if (offIcon) offIcon.style.display = 'none';
            }
        };

        const startMusic = () => {
            music.play().then(() => {
                updateMusicIcons();
                window.removeEventListener('click', startMusic);
                window.removeEventListener('scroll', startMusic);
            }).catch(e => {
                console.log("Autoplay blocked. Waiting for interaction.");
            });
        };

        if (navMusicToggle) {
            navMusicToggle.addEventListener('click', (e) => {
                e.preventDefault();
                if (music.paused) {
                    music.play();
                } else {
                    music.pause();
                }
                updateMusicIcons();
            });
        }

        // Delay start by 3 seconds
        setTimeout(startMusic, 3000);

        // Fallback: Start on first interaction if blocked
        window.addEventListener('click', startMusic);
        window.addEventListener('scroll', startMusic);
    }
});
