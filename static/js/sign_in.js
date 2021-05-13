$(function () {
    $('#user_password')[0].focus();



    // 根据窗口大小改变图片大小
    var window_height = $(window).height();
    var margin_height = (window_height - 400) / 2;
    $('#wrapper_border').css('margin', margin_height + 'px auto');


    $(window).resize(function () {
        var window_height = $(window).height();
        var margin_height = (window_height - 400) / 2;
        $('#wrapper_border').css('margin', margin_height + 'px auto');
    });
    // 根据窗口大小改变图片大小




    $('#user_password').on('keypress', function (ev) {
        if (ev.charCode == 13) {
            var password = $('#user_password').val();
            submit_password(password)
        }
    });


    $('#user_load_in').on('click', function () {
        var password = $('#user_password').val();
        submit_password(password)
    });

    function submit_password(password) {
        $.ajax({
            'url': '/check_out_passwd/',
            'type': 'post',
            'data': {
                'passwd': password
            },
            success: function (result) {
                if (result.code == '888') {
                    $('#passwd_error').css('visibility', 'hidden');
                    window.location.href = '/purchase/'
                }
                else {
                    $('#passwd_error').css('visibility', 'visible');
                }
            }
        })
    }

});