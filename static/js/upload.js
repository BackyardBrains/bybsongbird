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

    function show_audios_and_images(current, last_current) {
        if (last_current != 0) {
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_user').html('<p>original file</p>');
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_user_clean').html('<p>clean file</p>');
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_activity').html('<p>activity file</p>');
            $(".result_sub:eq(" + (last_current - 1) + ")").find('.audio_noise').html('<p>noise file</p>');
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

        $("#pagin li").first().find('a').addClass('current');
        
        $("#pagin").prepend('<span class="prev">Prev</span>');
        $("#pagin").append('<span class="next">Next</span>');

        $("#pagin").prepend('<span class="first">First</span>');
        $("#pagin").append('<span class="last">Last</span>');

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
        $("#pagin li a").on('click', function() {
            var last_current = $("#pagin li").find('.current').html();
            $("#pagin li").find('.current').removeClass('current');
            $(this).addClass('current');
            $(".ellipsis").remove();
            current = parseInt($(this).text());
            showNumber(current);
            showPage(current);
            show_audios_and_images(current, last_current);
        });

        $(".prev").on("click", function() {
          $(".ellipsis").remove();
          $("#pagin li").find('.current').removeClass('current');
          $("#pagin>li:eq("+ (current - 2) +")").find('a').addClass('current');
          current = current - 1;
          showNumber(current);
          showPage(current);
          show_audios_and_images(current, current + 1);
        });

        $(".next").on("click", function() {
          $(".ellipsis").remove();
          $("#pagin li").find('.current').removeClass('current');
          $("#pagin>li:eq("+ current +")").find('a').addClass('current');
          current = current + 1;
          showNumber(current);
          showPage(current);
          show_audios_and_images(current, current - 1);
        });

        $(".first").on("click", function() {
          $(".ellipsis").remove();
          var last_current = $("#pagin li").find('.current').html();
          $("#pagin li").find('.current').removeClass('current');
          $("#pagin li").first().find('a').addClass('current');
          showNumber(1);
          showPage(1);
          show_audios_and_images(1, last_current);
        });

        $(".last").on("click", function() {
          $(".ellipsis").remove();
          var last_current = $("#pagin li").find('.current').html();
          $("#pagin li").find('.current').removeClass('current');
          $("#pagin li").last().find('a').addClass('current');
          showNumber(pageCount);
          showPage(pageCount);
          show_audios_and_images(pageCount, last_current);
        });
    }
});

function donut_chart(data, color, chart) {
    var text = (data[0].value * 100).toFixed(3) + '%' ;
    var width = 90;
    var height = 90;
    var thickness = 10;

    var radius = Math.min(width, height) / 2;

    var svg = d3.select("#" + chart)
        .append('svg')
        .attr('class', 'pie')
        .attr('width', width)
        .attr('height', height);

    var g = svg.append('g')
        .attr('transform', 'translate(' + (width/2) + ',' + (height/2) + ')');

    var arc = d3.arc()
        .innerRadius(radius - thickness)
        .outerRadius(radius);

    var pie = d3.pie()
        .value(function(d) { return d.value; })
        .sort(null);

    var path = g.selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d,i) => color[i])


        g.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .style("font-size", "14px")
            .text(text);
}