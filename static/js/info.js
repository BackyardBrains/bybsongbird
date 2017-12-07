$(function() {
    $(document).on('click', function(event){
        if(!($(event.target).hasClass("audio_button") || $(event.target).hasClass("fa-play") || $(event.target).hasClass("audio_play"))) {
            if ($('.popup').is(':visible')) {
                $('.popup').hide();
                $('.black_overlay').hide();
            }
        } else {
            $('.popup').show();
            $('.black_overlay').show();
        }
    })
});