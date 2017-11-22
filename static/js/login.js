function login() {
    var username = $(".username").val();
    var password = $(".password").val();
    var remember = $("#rememberme").prop('checked');
    $.post("/api/login",
        {
            username: username,
            password: password,
            remember: remember
        },
        function (data, status) {
            window.location.href = "/";
        }, 'json').fail(function (data, status) {
        var error_message = data.responseJSON['error'];
        $(".error").text(error_message);
    });
}
