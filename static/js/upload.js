$(function() {
    $('#chooseFile').bind('change', function () {
        var size = $("#chooseFile")[0].files.length
        if (size > 1) {
            $("#noFile").text(size + ' files chosen'); 
        } else {
            var filename = $("#chooseFile").val();
            if (/^\s*$/.test(filename)) {
                $(".file-upload").removeClass('active');
                $("#noFile").text("No file chosen..."); 
            }
            else {
                $(".file-upload").addClass('active');
                $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
            }
        }
    });

    $('.location_icon').on('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                $('.latitude').val(position.coords.latitude);
                $('.longitude').val(position.coords.longitude);
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });

    $('.close_icon').on('click', function() {
        $('.result_title').hide();
    });
});