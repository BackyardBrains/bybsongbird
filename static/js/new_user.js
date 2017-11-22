function new_user() {
    var username = $(".username").val();
    var password = $(".password").val();
    var confirm_password = $(".confirm_password").val();
    var remember = $("#rememberme").prop('checked');
    $.post("/api/new_user",
        {
            username: username,
            password: password,
            confirm_password: confirm_password
        },
        function (data, status) {
            window.location.href = "/login";
        }, 'json').fail(function (data, status) {
        var error_message = data.responseJSON['error'];
        $(".error").text(error_message);
    });
}
