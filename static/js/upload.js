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

    // $('.location_icon').on('click', function() {
    //     if (navigator.geolocation) {
    //         navigator.geolocation.getCurrentPosition(function(position) {
    //             $('.latitude').val(position.coords.latitude);
    //             $('.longitude').val(position.coords.longitude);
    //         });
    //     } else {
    //         alert("Geolocation is not supported by this browser.");
    //     }
    // });

    $('.close_icon').on('click', function() {
        $('.result_title').hide();
    });

    $('.classification').each(function() {
        var thischart = d3.select(this)
        var data1 = JSON.parse($(this).attr('data-classification-first'));
        var color1 = ['#23CFEE', '#CACACA'];
        donut_chart(data1, color1, 'chart1', thischart);
        $(this).find('.first_match_intro').find('.match_name').html(data1[0]['name']);

        var data2 = JSON.parse($(this).attr('data-classification-second'));
        var color2 = ['#ED531D', '#CACACA'];
        donut_chart(data2, color2, 'chart2', thischart);
        $(this).find('.second_match_intro').find('.match_name').html(data2[0]['name']);

        var data3 = JSON.parse($(this).attr('data-classification-third'));
        var color3 = ['#ED0C19', '#CACACA'];
        donut_chart(data3, color3, 'chart3', thischart);
        $(this).find('.third_match_intro').find('.match_name').html(data3[0]['name']);
    });

    $('.info_location').each(function() {
        var thismap = $(this).find('.map');
        var sampleid = thismap.attr('data-sampleid');
        var longitude = thismap.attr('data-longitude');
        var latitude = thismap.attr('data-latitude');
        show_map(sampleid, latitude, longitude, thismap);
    });

    progress_bar_buttons();
    function progress_bar_buttons() {
        $('.humidity_button').each(function() {
            var humidity = $(this).attr('data-humidity');
            $(this).css('left', humidity + '%');
        })
        
        $('.temp_button').each(function() {
            var temp = $(this).attr('data-temp');
            $(this).css('left', temp + '%');
        })  
        
        $('.light_button').each(function() {
            var light = $(this).attr('data-light');
            $(this).css('left', light + '%');
        })  
    }

    function show_audios_and_images(current, last_current) {
        if (last_current != 0) {
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_user').empty();
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_user_clean').empty();
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_activity').empty();
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_noise').empty();
        }

        var waveform_user = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user').attr('data-user-waveform');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user').append('<img class="waveform" src=' + waveform_user + ' height="50px"/>');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user').append('<p class="result_text">Original Audio Track:</p>')
        var audio_user = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user').attr('data-audio-user');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user').append('<audio controls preload="metadata" class="audiofile"><source src="../static/songs/users/' + audio_user + '" type="audio/mpeg"></audio>');
                
        var waveform_user_clean = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user_clean').attr('data-user-clean-waveform');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user_clean').append('<img class="waveform" src=' + waveform_user_clean + ' height="50px"/>');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user_clean').append('<p class="result_text">Cleaned Audio Track:</p>')
        var audio_user_clean = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user_clean').attr('data-audio-user-clean');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_user_clean').append('<audio controls preload="metadata" class="audiofile"><source src=' + audio_user_clean + ' type="audio/mpeg"></audio>');

        var waveform_activity = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_activity').attr('data-activity-waveform');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_activity').append('<img class="waveform" src=' + waveform_activity + ' height="50px"/>');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_activity').append('<p class="result_text">Activity Audio Track:</p>')
        var audio_activity = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_activity').attr('data-audio-activity');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_activity').append('<audio controls preload="metadata" class="audiofile"><source src=' + audio_activity + ' type="audio/mpeg"></audio>');

        var waveform_noise = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_noise').attr('data-noise-waveform');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_noise').append('<img class="waveform" src=' +waveform_noise + ' height="50px" />');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_noise').append('<p class="result_text">Noise Audio Track:</p>')
        var audio_noise = $(".result_sub:eq(" + (current - 1) + ")").find('.audio_noise').attr('data-audio-noise');
        $(".result_sub:eq(" + (current - 1) + ")").find('.audio_noise').append('<audio controls preload="metadata" class="audiofile"><source src=' + audio_noise + ' type="audio/mpeg"></audio>');
    }

    pagination();
    function pagination() {
        var pageSize = 1;
        var pageCount = Math.ceil($(".result_sub").length / pageSize);

        for (var i = 0; i < pageCount; i++){
          $("#pagin").append('<li class="paging"><a href="#" class="paging_num">'+(i+1)+'</a></li>');
        }

        $("#pagin li").first().addClass('current');
        
        $("#pagin").prepend('<div class="prev">&#8249;</div>');
        $("#pagin").append('<div class="next">&#8250;</div>');

        $("#pagin").prepend('<div class="first">&laquo;</div>');
        $("#pagin").append('<div class="last">&raquo;</div>');

        showPage = function(page) {
          $(".result_sub").hide();
          $(".result_sub").each(function(n) {
            if (n >= pageSize * (page - 1) && n < pageSize * page)
              $(this).show();
          }); 
        }

        showNumber = function(current) {
          if (current > 1) {
            $(".prev").show();
          } else {
            $(".prev").hide();
          }

          if (current == pageCount) {
            $(".next").hide()
          } else {
            $(".next").show()
          }

          if (pageCount > 10) {
            $(".paging").hide();
            $(".paging").each(function() {
              var paging = parseInt($(this).text());
              if (current < 5) {
                if (paging <= 5 ) {
                  $(this).show();
                }
              } else if (current <= pageCount - 8){
                if (paging >= current - 2 && paging <= current + 2 ) {
                  $(this).show();
                }
              } else {
                if (paging > pageCount - 10 && paging < pageCount - 2) {
                  $(this).show();
                }
              }
              if (paging <= pageCount && paging >= pageCount - 2) {
                $(this).show();
              }
            });
            if (current < 5) {
              $("#pagin>li:eq(4)").append('<li class="ellipsis">......</li>');
            } else if (current <= pageCount - 8){
              $("#pagin>li:eq("+ (current+1) +")").append('<li class="ellipsis">......</li>');
            }
          }
        }
        
        showNumber(1);
        showPage(1);

        var current = 1;
        show_audios_and_images(current, 0);
        $("#pagin li").on('click', function() {
            var last_current = $("#pagin").find('.current').find('a').html();
            $("#pagin").find('.current').removeClass('current');
            $(this).addClass('current');
            $(".ellipsis").remove();
            current = parseInt($(this).text());
            showNumber(current);
            showPage(current);
            show_audios_and_images(current, last_current);
        });

        $(".prev").on("click", function() {
          $(".ellipsis").remove();
          $("#pagin").find('.current').removeClass('current');
          $("#pagin>li:eq("+ (current - 2) +")").addClass('current');
          current = current - 1;
          showNumber(current);
          showPage(current);
          show_audios_and_images(current, current + 1);
        });

        $(".next").on("click", function() {
          $(".ellipsis").remove();
          $("#pagin").find('.current').removeClass('current');
          $("#pagin>li:eq("+ current +")").addClass('current');
          current = current + 1;
          showNumber(current);
          showPage(current);
          show_audios_and_images(current, current - 1);
        });

        $(".first").on("click", function() {
          $(".ellipsis").remove();
          var last_current = $("#pagin").find('.current').find('a').html();
          $("#pagin").find('.current').removeClass('current');
          $("#pagin li").first().addClass('current');
          showNumber(1);
          showPage(1);
          show_audios_and_images(1, last_current);
        });

        $(".last").on("click", function() {
          $(".ellipsis").remove();
          var last_current = $("#pagin").find('.current').find('a').html();
          $("#pagin").find('.current').removeClass('current');
          $("#pagin li").last().addClass('current');
          showNumber(pageCount);
          showPage(pageCount);
          show_audios_and_images(pageCount, last_current);
        });
    }
});