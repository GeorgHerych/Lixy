const carousels = document.querySelectorAll('.carousel');

carousels.forEach(carousel => {
    carousel.addEventListener('slid.bs.carousel', function () {
        const videos = carousel.querySelectorAll('video');

        videos.forEach(video => {
            video.pause();
            video.currentTime = 0;
        });
    });
});