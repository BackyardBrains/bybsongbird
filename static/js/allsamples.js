if (sessionStorage.getItem("sort") != null || sessionStorage.getItem("dir") != null){
    document.getElementById("sortid").selectedIndex = sessionStorage.getItem("sort");
    document.getElementById("dirid").selectedIndex = sessionStorage.getItem("dir");
}

function submitThis() {
    sessionStorage.setItem("sort", document.getElementById("sortid").selectedIndex);
    sessionStorage.setItem("dir", document.getElementById("dirid").selectedIndex);

    document.getElementById("selection").submit();
}

$(function () {
    pagination();
    function pagination() {
        var pageSize = 20;
        var pageCount = Math.ceil($(".result_sub").length / pageSize);

        for (var i = 0; i < pageCount; i++) {
            $("#pagin").append('<li class="paging"><a href="#" class="paging_num">' + (i + 1) + '</a></li>');
        }

        $("#pagin li").first().addClass('current');

        $("#pagin").prepend('<div class="prev">&#8249;</div>');
        $("#pagin").append('<div class="next">&#8250;</div>');

        $("#pagin").prepend('<div class="first">&laquo;</div>');
        $("#pagin").append('<div class="last">&raquo;</div>');

        showPage = function (page) {
            $(".result_sub").hide();
            $(".result_sub").each(function (n) {
                if (n >= pageSize * (page - 1) && n < pageSize * page)
                    $(this).show();
            });
        }

        showNumber = function (current) {
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
                $(".paging").each(function () {
                    var paging = parseInt($(this).text());
                    if (current < 5) {
                        if (paging <= 5) {
                            $(this).show();
                        }
                    } else if (current <= pageCount - 8) {
                        if (paging >= current - 2 && paging <= current + 2) {
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
                } else if (current <= pageCount - 8) {
                    $("#pagin>li:eq(" + (current + 1) + ")").append('<li class="ellipsis">......</li>');
                }
            }
        }

        showNumber(1);
        showPage(1);

        var current = 1;
        show_audios_and_images(current, 0);
        $("#pagin li").on('click', function () {
            var last_current = $("#pagin").find('.current').find('a').html();
            $("#pagin").find('.current').removeClass('current');
            $(this).addClass('current');
            $(".ellipsis").remove();
            current = parseInt($(this).text());
            showNumber(current);
            showPage(current);
            show_audios_and_images(current, last_current);
        });

        $(".prev").on("click", function () {
            $(".ellipsis").remove();
            $("#pagin").find('.current').removeClass('current');
            $("#pagin>li:eq(" + (current - 2) + ")").addClass('current');
            current = current - 1;
            showNumber(current);
            showPage(current);
            show_audios_and_images(current, current + 1);
        });

        $(".next").on("click", function () {
            $(".ellipsis").remove();
            $("#pagin").find('.current').removeClass('current');
            $("#pagin>li:eq(" + current + ")").addClass('current');
            current = current + 1;
            showNumber(current);
            showPage(current);
            show_audios_and_images(current, current - 1);
        });

        $(".first").on("click", function () {
            $(".ellipsis").remove();
            var last_current = $("#pagin").find('.current').find('a').html();
            $("#pagin").find('.current').removeClass('current');
            $("#pagin li").first().addClass('current');
            showNumber(1);
            showPage(1);
            show_audios_and_images(1, last_current);
        });

        $(".last").on("click", function () {
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