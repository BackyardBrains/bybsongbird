$(function() {
    $('.header').on('click', function() {
        $('.header').each(function() {
            if ($(this).hasClass('active')) {
                var desc_no = $(this).attr('data-associated');
                $('.' + desc_no).hide();
                $(this).removeClass('active');
            }
        });
        $(this).addClass('active');
        var desc_no = $(this).attr('data-associated');
        $('.' + desc_no).show();
    });
});