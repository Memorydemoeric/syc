$(function () {
   $('#power_off').on('click', function (ev) {
       ev.preventDefault();
       Ewin.confirm({message: '确认关闭服务器？'}).on(function (e) {
           if (e) {
               window.location.href = '/system/power_off/'
           }
       })
   });

    $('#clear_temp').on('click', function (ev) {
        ev.preventDefault();
        Ewin.confirm({message: '是否清理缓存信息？'}).on(function (e) {
            if (e) {
                $.ajax({
                    'url': '/system/clear_temp_xlsx/',
                    'type': 'post',
                    'data': {'operate_code': 'ok'},
                    success: function (result) {
                        if (result.code == '888') {
                            Ewin.alert({message: '清理成功!'})
                        }
                    }
                })
            }
        })
    })
});