$(function () {
    $('form').each(function () {
        $(this).find('crit').keypress(function (e) {
            if (e.which == 10 || e.which == 13) {
                this.form.submit();
            }
        });

        $(this).find('input[type=submit]').hide();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var sort = document.getElementById('sortid');
    var dir = document.getElementById('dirid');
    var col = document.getElementById('colid');
    var equ = document.getElementById('equid');
    var text = document.getElementById('textid');

    if (sessionStorage['sortid']) {
        input.value = sessionStorage['sortid'];
    }
    if (sessionStorage['dirid']) {
        input.value = sessionStorage['dirid'];
    }
    if (sessionStorage['colid']) {
        input.value = sessionStorage['colid'];
    }
    if (sessionStorage['equid']) {
        input.value = sessionStorage['equid'];
    }
    if (sessionStorage['textid']) {
        input.value = sessionStorage['textid'];
    }

    input.onchange = function () {
        sessionStorage['sortid'] = this.value;
        sessionStorage['dirid'] = this.value;
        sessionStorage['colid'] = this.value;
        sessionStorage['equid'] = this.value;
        sessionStorage['textid'] = this.value;
    }
});