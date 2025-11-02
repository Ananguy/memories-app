document.addEventListener('DOMContentLoaded', function() {
    // Create lightbox elements
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <span class="close-lightbox">&times;</span>
            <div class="media-container"></div>
            <a class="download-btn" download>
                <svg viewBox="0 0 24 24" width="24" height="24">
                    <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
                </svg>
                Download
            </a>
        </div>
    `;
    document.body.appendChild(lightbox);

    // Get lightbox elements
    const mediaContainer = lightbox.querySelector('.media-container');
    const downloadBtn = lightbox.querySelector('.download-btn');
    const closeBtn = lightbox.querySelector('.close-lightbox');

    // Add click handlers to all media items
    document.querySelectorAll('.media-item').forEach(item => {
        const mediaElement = item.querySelector('img, video, .video-container');
        if (mediaElement) {
            mediaElement.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent default video play
                openLightbox(mediaElement);
            });
        }
    });

    // Open lightbox
    function openLightbox(mediaElement) {
        const isVideo = mediaElement.tagName.toLowerCase() === 'video' || mediaElement.classList.contains('video-container');
        let lightboxMedia;

        if (isVideo) {
            lightboxMedia = document.createElement('video');
            const videoSrc = mediaElement.tagName.toLowerCase() === 'video' ?
                mediaElement.querySelector('source').src :
                mediaElement.querySelector('video source').src;
            lightboxMedia.src = videoSrc;
            lightboxMedia.controls = true;
            lightboxMedia.autoplay = true;
        } else {
            lightboxMedia = document.createElement('img');
            lightboxMedia.src = mediaElement.src;
        }

        // Clear previous content and add new media
        mediaContainer.innerHTML = '';
        mediaContainer.appendChild(lightboxMedia);

        // Update download button
        const downloadSrc = isVideo ?
            (mediaElement.tagName.toLowerCase() === 'video' ?
                mediaElement.querySelector('source').src :
                mediaElement.querySelector('video source').src) :
            mediaElement.src;
        downloadBtn.href = downloadSrc;
        downloadBtn.download = downloadBtn.href.split('/').pop();

        // Show lightbox
        lightbox.classList.add('active');

        // Add ESC key handler
        document.addEventListener('keydown', handleEscKey);
    }

    // Close lightbox
    function closeLightbox() {
        lightbox.classList.remove('active');
        const video = mediaContainer.querySelector('video');
        if (video) video.pause();
        document.removeEventListener('keydown', handleEscKey);
    }

    // Close on click outside
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    // Close on X button click
    closeBtn.addEventListener('click', closeLightbox);

    // Close on ESC key
    function handleEscKey(e) {
        if (e.key === 'Escape') closeLightbox();
    }
});
