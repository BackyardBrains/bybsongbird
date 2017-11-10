$(function() {
    navbar_control();
    function navbar_control() {
        var current = location.pathname;
        $('.nav-link').each(function(){
            if($(this).attr('href') == current){
                $(this).addClass('active');
            }
        });
    }

    $('.nav-link').on('click', function() {
        $('.nav-link').each(function() {
            if ($(this).hasClass('active')) {
                console.log('has activate')
                $(this).removeClass('active');
            }
        });
        $(this).addClass('active');
    });
});