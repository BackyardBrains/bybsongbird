function submitNewPassword() {
    var old_password = $(".old_password").val();
    var new_password = $(".new_password").val();
    var confirm_new_password = $(".confirm_new_password").val();
    $.post("/api/change-password",
        {
            old_password: old_password,
            new_password: new_password,
            confirm_new_password: confirm_new_password
        },
        function (data, status) {
            var success_message = data['success'];
            $(".error").hide();
            $(".success").show();
            $(".success").text(success_message);
        }, 'json').fail(function (data, status) {
        var error_message = data.responseJSON['error'];
        $(".success").hide();
        $(".error").show();
        $(".error").text(error_message);
    });
}
