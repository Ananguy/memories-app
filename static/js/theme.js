document.addEventListener('DOMContentLoaded', function() {
    let heartInterval = null; // Define heartInterval at the top level
    
    // Create theme switcher
    const themeSwitcher = document.createElement('div');
    themeSwitcher.className = 'theme-switcher';
    themeSwitcher.innerHTML = `
        <button class="theme-btn" data-theme="light">☀️</button>
        <button class="theme-btn" data-theme="dark">🌙</button>
        <button class="theme-btn" data-theme="rom">💝</button>
    `;
    document.body.appendChild(themeSwitcher);

    // Set dark mode as default
    document.body.classList.add('dark-mode');

    // Add mini hearts animation to rom mode button
    const romButton = themeSwitcher.querySelector('[data-theme="rom"]');
    let miniHeartInterval;

    function createMiniHeart() {
        const heart = document.createElement('div');
        heart.className = 'mini-heart';
        heart.textContent = '💖';
        heart.style.setProperty('--tx', ((Math.random() - 0.5) * 20) + 'px');
        romButton.appendChild(heart);
        
        // Remove the heart after animation completes
        heart.addEventListener('animationend', () => heart.remove());
    }

    function startMiniHearts() {
        createMiniHeart();
        miniHeartInterval = setInterval(createMiniHeart, 200);
    }

    function stopMiniHearts() {
        if (miniHeartInterval) {
            clearInterval(miniHeartInterval);
            miniHeartInterval = null;
        }
    }

    romButton.addEventListener('mouseenter', startMiniHearts);
    romButton.addEventListener('mouseleave', stopMiniHearts);

    // Create floating hearts container
    const heartsContainer = document.createElement('div');
    heartsContainer.className = 'floating-hearts';
    document.body.appendChild(heartsContainer);

    // Create audio element for rom mode
    const audioElement = document.createElement('audio');
    audioElement.id = 'bg-music';
    audioElement.loop = true;
    audioElement.src = '/static/music/love-story.mp3.mp3'; // Indila - Love Story
    audioElement.volume = 0.4; // Set initial volume to 40%
    document.body.appendChild(audioElement);

    // Add volume control for music
    const volumeControl = document.createElement('div');
    volumeControl.className = 'volume-control';
    volumeControl.innerHTML = `
        <button class="volume-btn">🔊</button>
        <input type="range" class="volume-slider" min="0" max="100" value="50">
    `;
    document.body.appendChild(volumeControl);

    // Handle volume control
    const volumeBtn = volumeControl.querySelector('.volume-btn');
    const volumeSlider = volumeControl.querySelector('.volume-slider');
    let isMuted = false;

    volumeBtn.addEventListener('click', () => {
        isMuted = !isMuted;
        audioElement.muted = isMuted;
        volumeBtn.textContent = isMuted ? '🔇' : '🔊';
    });

    volumeSlider.addEventListener('input', (e) => {
        const volume = e.target.value / 100;
        audioElement.volume = volume;
        volumeBtn.textContent = volume === 0 ? '🔇' : '🔊';
    });

    // Show/hide volume control based on theme
    function toggleVolumeControl(theme) {
        volumeControl.style.display = theme === 'rom' ? 'flex' : 'none';
    }

    // Theme switching functionality
    const themeButtons = document.querySelectorAll('.theme-btn');
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Set initial theme
    setTheme(savedTheme);

    // Resume music if it was playing in rom mode
    if (savedTheme === 'rom' && localStorage.getItem('musicPlaying') === 'true') {
        playBackgroundMusic();
    }

    themeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.theme;
            setTheme(theme);
        });
    });

    function setTheme(theme) {
        // First, stop any existing animations
        stopHeartAnimation();
        stopBackgroundMusic();

        // Remove all theme classes
        document.body.classList.remove('light-mode', 'dark-mode', 'rom-mode');
        
        // Add new theme class
        document.body.classList.add(`${theme}-mode`);
        
        // Handle rom mode specific features
        if (theme === 'rom') {
            startHeartAnimation();
            playBackgroundMusic();
        }

        localStorage.setItem('theme', theme);
        updateActiveButton(theme);
    }

    function updateActiveButton(theme) {
        themeButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.theme === theme);
        });
    }

    // Heart animation functions
    function createHeart() {
        const heart = document.createElement('div');
        heart.className = 'heart';
        heart.innerHTML = '💖';
        
        // Random horizontal position across the screen
        heart.style.left = Math.random() * 100 + 'vw';
        
        // Start from a random position above the screen
        heart.style.top = (-10 - Math.random() * 20) + 'vh';
        
        heartsContainer.appendChild(heart);
        
        // Remove heart after animation completes
        heart.addEventListener('animationend', () => {
            heart.remove();
        });
    }

    function startHeartAnimation() {
        stopHeartAnimation();
        
        // Clear any existing hearts
        heartsContainer.innerHTML = '';
        heartsContainer.style.display = 'block';
        
        // Create initial set of hearts
        for(let i = 0; i < 30; i++) {
            setTimeout(() => createHeart(), i * 100);
        }
        
        // Continue creating hearts at regular intervals (every 200ms for more density)
        heartInterval = setInterval(createHeart, 200);
    }

    function createExplosionHeart(startX, startY) {
        const heart = document.createElement('div');
        heart.className = 'heart explosion-heart';
        heart.innerHTML = '💖';
        
        // Random direction
        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 100 + 50;
        
        // Calculate end position
        const endX = startX + Math.cos(angle) * distance;
        const endY = startY + Math.sin(angle) * distance;
        
        // Set size and position
        heart.style.fontSize = (8 + Math.random() * 4) + 'px';
        heart.style.position = 'fixed';
        heart.style.left = startX + 'px';
        heart.style.top = startY + 'px';
        
        // Add animation
        heart.style.animation = 'none';
        heart.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
        heart.style.opacity = '0';
        
        heartsContainer.appendChild(heart);
        
        // Trigger animation
        setTimeout(() => {
            heart.style.transform = `translate(${endX - startX}px, ${endY - startY}px) scale(1)`;
            heart.style.opacity = '1';
        }, 10);
        
        // Remove after animation
        setTimeout(() => heart.remove(), 1000);
    }

    function stopHeartAnimation() {
        if (heartInterval) {
            clearInterval(heartInterval);
            heartInterval = null;
        }
        if (heartsContainer) {
            heartsContainer.innerHTML = '';
            heartsContainer.style.display = 'none';
        }
    }

    // Music functions
    function playBackgroundMusic() {
        const audio = document.getElementById('bg-music');
        if (audio.src) {
            const savedTime = localStorage.getItem('musicTime');
            if (savedTime) {
                audio.currentTime = parseFloat(savedTime);
            }
            // Ensure audio is loaded before playing
            if (audio.readyState >= 2) {
                audio.play().catch(e => console.log('Autoplay blocked:', e));
            } else {
                audio.addEventListener('canplay', () => {
                    audio.play().catch(e => console.log('Autoplay blocked:', e));
                }, { once: true });
            }
            localStorage.setItem('musicPlaying', 'true');
        }
    }

    function stopBackgroundMusic() {
        const audio = document.getElementById('bg-music');
        localStorage.setItem('musicTime', audio.currentTime);
        audio.pause();
        localStorage.setItem('musicPlaying', 'false');
    }

    // Set music source (you'll need to provide the actual music file)
    function setBackgroundMusic(musicUrl) {
        const audio = document.getElementById('bg-music');
        audio.src = musicUrl;
    }

    // Expose function to set music
    window.setBackgroundMusic = setBackgroundMusic;
});
