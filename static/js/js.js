        // Update current program display immediately
        function updateNowPlaying() {
            fetch('/api/current-program/')
                .then(response => response.json())
                .then(data => {
                    let displayText = '';
                    if (data.status === 'live') {
                        displayText = `🔴 LIVE: ${data.title} - ${data.host || 'Energy Radio'}`;
                    } else if (data.status === 'upcoming') {
                        displayText = `⏭️ NEXT: ${data.title} at ${data.start_time}`;
                    } else if (data.status === 'later') {
                        displayText = `📻 ${data.title} at ${data.start_time}`;
                    } else {
                        displayText = 'Tune in to Energy Radio';
                    }
                    const element = document.getElementById('nowPlayin');
                    if (element) {
                        element.textContent = displayText;
                    }
                })
                .catch(error => {
                    console.error('Error fetching program:', error);
                    const element = document.getElementById('nowPlayin');
                    if (element) {
                        element.textContent = 'Tune in to Energy Radio';
                    }
                });
        }

        function updateNowPlayingProgram() {
            updateNowPlaying();
            if (typeof refreshLiveProgramBadges === 'function') {
                refreshLiveProgramBadges();
            }
        }

        // Update immediately on page load
        updateNowPlaying();
        
        // Update every 60 seconds
        setInterval(updateNowPlaying, 60000);

        $(document).ready(function(){
            // Hero taglines - rotate every 7 seconds
            const heroTaglines = [
                "Powering Rwanda's Voice, Rhythm & Community",
                "Your home for music, entertainment, youth inspiration, and impactful communication across Rwanda.",
                "Tune in. Engage. Feel the ENERGY."
            ];
            let currentTaglineIndex = 0;
            const heroTaglineElement = $('#heroTagline');
            
            function displayTagline(text) {
                heroTaglineElement.fadeOut(300, function() {
                    $(this).text(text);
                    // Trigger slide-up animation by removing and re-adding the class
                    $(this).removeClass('slideInText');
                    // Force reflow to restart animation
                    void $(this)[0].offsetWidth;
                    $(this).addClass('slideInText').fadeIn(300);
                });
            }
            
            // Display first tagline immediately with animation
            heroTaglineElement.text(heroTaglines[0]).addClass('slideInText');
            
            // Rotate taglines every 7 seconds
            setInterval(function() {
                currentTaglineIndex = (currentTaglineIndex + 1) % heroTaglines.length;
                displayTagline(heroTaglines[currentTaglineIndex]);
            }, 7000);
            
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
            
         // Audio player - Global state for synchronization
window.isPlaying = false;
const audio = document.getElementById("radio-audio-player");

$('#playBtn').click(function () {
    if (!window.isPlaying) {
        audio.play();                 // ▶ PLAY STREAM
        $(this).html('<i class="fas fa-pause"></i>');
        window.isPlaying = true;
    } else {
        audio.pause();                // ⏸ PAUSE STREAM
        $(this).html('<i class="fas fa-play"></i>');
        window.isPlaying = false;
    }
});
// Volume slider
$('.volume-slider').on('input', function () {
    audio.volume = $(this).val() / 100;

    // Optional: auto mute if slider is 0
    if (audio.volume == 0) {
        audio.muted = true;
        $('#muteBtn').removeClass('fa-volume-up').addClass('fa-volume-mute');
    } else {
        audio.muted = false;
        $('#muteBtn').removeClass('fa-volume-mute').addClass('fa-volume-up');
    }
});

// 🔊 Mute / Unmute button
$('#muteBtn').click(function () {
    audio.muted = !audio.muted;

    if (audio.muted) {
        $(this).removeClass('fa-volume-up').addClass('fa-volume-mute');
    } else {
        $(this).removeClass('fa-volume-mute').addClass('fa-volume-up');
    }
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

            
            // Update now playing on page load (use slight delay to ensure DOM is ready)
            console.log('Setting up now playing updates');
            setTimeout(function() {
                console.log('Calling updateNowPlayingProgram');
                refreshLiveProgramBadges();
                updateNowPlayingProgram();
                // Update every 60 seconds (1 minute)
                setInterval(refreshLiveProgramBadges, 60000);
                setInterval(updateNowPlayingProgram, 60000);
            }, 500);

            function refreshLiveProgramBadges() {
                fetch('/api/current-program/')
                    .then(response => response.json())
                    .then(data => {
                        const programSlides = $('.program-slide');
                        if (!programSlides.length) {
                            return;
                        }

                        if (data.status === 'live' && data.title) {
                            const liveTitle = String(data.title).trim();

                            programSlides.each(function() {
                                const slide = $(this);
                                const title = String(slide.data('program-title') || '').trim();
                                const card = slide.find('.program-card-slide');
                                const cardHasBadge = card.find('> .live-badge').length;

                                if (title === liveTitle) {
                                    slide.addClass('is-live');
                                    card.addClass('is-live');
                                    if (!cardHasBadge) {
                                        card.append('<span class="live-badge">LIVE NOW</span>');
                                    } else {
                                        card.find('> .live-badge').show();
                                    }
                                } else {
                                    slide.removeClass('is-live');
                                    card.removeClass('is-live');
                                    const badge = card.find('> .live-badge');
                                    if (badge.length) {
                                        badge.hide();
                                    }
                                }
                            });

                            const liveSlide = programSlides.filter(function() {
                                return String($(this).data('program-title') || '').trim() === liveTitle;
                            }).first();

                            if (liveSlide.length) {
                                currentProgramIndex = liveSlide.index();
                                updateSliderPosition(currentProgramIndex);
                            }
                        } else {
                            programSlides.each(function() {
                                const slide = $(this);
                                const card = slide.find('.program-card-slide');
                                const badge = card.find('> .live-badge');
                                slide.removeClass('is-live');
                                card.removeClass('is-live');
                                if (badge.length) {
                                    badge.hide();
                                }
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Error refreshing live program badges:', error);
                    });
            }

            // Programs Slider
            const programSlides = $('.program-slide');
            let currentProgramIndex = programSlides.filter('.is-live').first().index();
            if (currentProgramIndex < 0) {
                currentProgramIndex = 0;
            }
            const totalPrograms = programSlides.length;
            const slider = $('#programsSlider');

            function updateSliderPosition(index = currentProgramIndex) {
                if (!programSlides.length) {
                    return;
                }

                const safeIndex = Math.max(0, Math.min(index, programSlides.length - 1));
                const wrapperWidth = slider.parent().width();
                const computedSliderStyle = getComputedStyle(slider[0]);
                const gap = parseFloat(computedSliderStyle.gap || 0);

                let leftOffset = 0;
                for (let i = 0; i < safeIndex; i += 1) {
                    const slide = programSlides.eq(i);
                    if (slide.length) {
                        leftOffset += slide.outerWidth(true);
                        leftOffset += gap;
                    }
                }

                const targetSlide = programSlides.eq(safeIndex);
                const targetWidth = targetSlide.length ? targetSlide.outerWidth(true) : 0;
                const targetWidthRaw = targetSlide.length ? targetSlide.outerWidth() : 0;
                const centerPosition = leftOffset + (targetWidth / 2);
                const offset = Math.round((wrapperWidth / 2) - centerPosition);

                slider.css('transform', `translateX(${offset}px)`);

                programSlides.removeClass('active');
                programSlides.eq(safeIndex).addClass('active');
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

        // Function to play livestream from hero section buttons
        function playLivestream(event) {
            event.preventDefault();
            
            // Get the audio player and play button
            const audio = document.getElementById("radio-audio-player");
            const playBtn = document.getElementById("playBtn");
            
            if (audio && playBtn) {
                // Toggle play/pause
                if (audio.paused) {
                    audio.play().then(() => {
                        // Update play button to show pause icon
                        playBtn.innerHTML = '<i class="fas fa-pause"></i>';
                        window.isPlaying = true;
                        
                        // Scroll to show the player
                        const playerFixed = document.querySelector('.audio-player-fixed');
                        if (playerFixed) {
                            playerFixed.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        }
                    }).catch(error => {
                        console.error('Error playing stream:', error);
                    });
                } else {
                    audio.pause();
                    playBtn.innerHTML = '<i class="fas fa-play"></i>';
                    window.isPlaying = false;
                }
            }
        }