$(function () {
    $('#cancel_storage_in').click(function () {
        window.location.href = '/storage/half_storage_in/'
    });

    $('#submit_storage_in').click(function () {
        Ewin.confirm({message: "确定半成品入库操作？"}).on(function (e) {
            if (!e) {
                window.location.href = '';
            }
            else {
                window.location.href = '/storage/half_storage_in_submit/';
            }
        });

    })


});