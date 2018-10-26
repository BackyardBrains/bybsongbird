$(function() {
    $(document).on('click', function(event){
        if(!($(event.target).hasClass("audio_button") || $(event.target).hasClass("fa-play") || $(event.target).hasClass("audio_play") || $(event.target).hasClass("match_name"))) {
            if ($('.popup').is(':visible')||$('.wiki').is(':visible')) {
                $('.popup').hide();
                $('.wiki').hide();
                $('.black_overlay').hide();
            }
        }

	else {
		if ($(event.target).hasClass("match_name")){
           	// Get different birds' name
		var birdname = event.target.innerHTML;
            	var url = "https://en.wikipedia.org/wiki/" + birdname + "?printable=yes";
		//alert(url);
		window.frames["wikiframe"].src = url;
		
		if ($('.popup').is(':visible')) {
                $('.popup').hide();
                $('.black_overlay').hide();
            }

            else {
                $('.wiki').show();
           		$('.black_overlay').show();
            }
        }

        else{
           $('.popup').show();
           $('.black_overlay').show();
        }
        
       	}
    })
});


