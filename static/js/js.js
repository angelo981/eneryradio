        $(document).ready(function(){
            // News Ticker Auto Slide
            let currentNewsIndex = 0;
            const newsSlides = $('.news-ticker-slide-full');
            const totalNewsSlides = newsSlides.length;
            
            function changeNewsSlide() {
                newsSlides.eq(currentNewsIndex).removeClass('active');
                currentNewsIndex = (currentNewsIndex + 1) % totalNewsSlides;
                newsSlides.eq(currentNewsIndex).addClass('active');
            }
            
            setInterval(changeNewsSlide, 5000);

            // Close News Ticker
            $('#closeNewsTicker').click(function() {
                $('#newsTickerWrapper').addClass('hidden');
                $('.hero-section').css('margin-top', '70px');
            });

            // Hero Slider
            let currentSlide = 0;
            const slides = $('.hero-slide');
            const totalSlides = slides.length;
            
            function displayText(element, text) {
                element.text(text);
                // Trigger animation by removing and re-adding the animation
                element.css('animation', 'none');
                setTimeout(() => {
                    element.css('animation', 'slideInText 0.8s ease-out forwards');
                }, 10);
            }
            
            function changeSlide() {
                slides.eq(currentSlide).removeClass('active');
                currentSlide = (currentSlide + 1) % totalSlides;
                slides.eq(currentSlide).addClass('active');
                
                const currentTypingElement = $('#typingText' + (currentSlide + 1));
                if (currentTypingElement.length) {
                    setTimeout(() => displayText(currentTypingElement, currentTypingElement.data('text')), 300);
                }
            }
            
            setInterval(changeSlide, 7000);
            
         // Audio player
let isPlaying = false;
const audio = document.getElementById("radio-audio-player");

$('#playBtn').click(function () {

    if (!isPlaying) {
        audio.play();                 // ▶ PLAY STREAM
        $(this).html('<i class="fas fa-pause"></i>');
        isPlaying = true;
    } else {
        audio.pause();                // ⏸ PAUSE STREAM
        $(this).html('<i class="fas fa-play"></i>');
        isPlaying = false;
    }

});
$('.volume-slider').on('input', function () {
    audio.volume = $(this).val() / 100;
});

            // Smooth scrolling
            $('a[href^="#"]').on('click', function(e) {
                e.preventDefault();
                const target = $(this.getAttribute('href'));
                if(target.length) {
                    $('html, body').stop().animate({
                        scrollTop: target.offset().top - 140
                    }, 1000);
                }
            });

            // Dynamic Now Playing
            const songs = [
                "pom pom - Bruce Melodie",
                "Ndakwemera - The Ben",
                "Malaika - Ariel Wayz",
                "Byambere - Meddy",
                "Champion - Nel Ngabo"
            ];
            let currentSong = 0;
            
            setInterval(function() {
                currentSong = (currentSong + 1) % songs.length;
                $('#nowPlaying, #nowPlaying2, #nowPlaying3').fadeOut(300, function() {
                    $(this).text(songs[currentSong]).fadeIn(300);
                });
            }, 10000);

            // Programs Slider
            let currentProgramIndex = 0;
            const programSlides = $('.program-slide');
            const totalPrograms = programSlides.length;
            const slider = $('#programsSlider');
            
            function updateSliderPosition() {
                const slideWidth = programSlides.eq(0).outerWidth(true);
                const offset = -currentProgramIndex * slideWidth + (slider.parent().width() / 2) - (slideWidth / 2);
                slider.css('transform', `translateX(${offset}px)`);
                programSlides.removeClass('active');
                programSlides.eq(currentProgramIndex).addClass('active');
            }
            
            setTimeout(() => updateSliderPosition(), 100);
            
            $('#nextBtn').click(function() {
                if (currentProgramIndex < totalPrograms - 1) {
                    currentProgramIndex++;
                    updateSliderPosition();
                }
            });
            
            $('#prevBtn').click(function() {
                if (currentProgramIndex > 0) {
                    currentProgramIndex--;
                    updateSliderPosition();
                }
            });
            
            programSlides.click(function() {
                currentProgramIndex = $(this).index();
                updateSliderPosition();
            });
            
            $(window).resize(function() {
                updateSliderPosition();
            });
            
            // Combined Modal & Tabs
            $('#interactionBtn').click(function() {
                $('#combinedModal').toggleClass('active');
            });
            
            $('#closeModal').click(function() {
                $('#combinedModal').removeClass('active');
            });
            
            // Tab Switching
            $('.modal-tab').click(function() {
                const tabName = $(this).data('tab');
                
                $('.modal-tab').removeClass('active');
                $(this).addClass('active');
                
                $('.tab-content-panel').removeClass('active');
                $('#' + tabName + 'Panel').addClass('active');
            });
            
            // Song Request Form
            $('#songRequestForm').submit(function(e) {
                e.preventDefault();
                const name = $('#requesterName').val();
                const song = $('#songName').val();
                alert(`Thank you ${name}! Your request for "${song}" has been submitted.`);
                this.reset();
                $('#combinedModal').removeClass('active');
            });
            
            // Message Form
            $('#messageForm').submit(function(e) {
                e.preventDefault();
                const message = $('#messageText').val();
                alert(`Thank you! Your message has been sent successfully.`);
                this.reset();
                $('#combinedModal').removeClass('active');
            });
            
            // Close modal when clicking outside
            $(document).click(function(e) {
                if (!$(e.target).closest('.custom-modal, .floating-btn').length) {
                    $('.custom-modal').removeClass('active');
                }
            });
        });