$(function () {
    $('#search_date_submit').on('click', function () {
        var start_time = $('#start_time').val();
        var end_time = $('#end_time').val();
        var select_type = $('#select_type').val();
        if (select_type == 'product') {
            window.location.href = '/report/report_storage_in_product/?start_time=' + start_time + '&end_time=' + end_time;
        }
        else if (select_type == 'half') {
            window.location.href = '/report/report_storage_in_half/?start_time=' + start_time + '&end_time=' + end_time;
        }
    });


    $('.storage_in_recover').on('click', function (ev) {
        ev.preventDefault();
        var $select_tr = $(this).parents('tr');
        var storage_in_id = $select_tr.attr('storage_in_id');
        var select_type = $('#select_type').val();
        var type_translate;
        if (select_type == 'half') {
            type_translate = '半成品'
        }
        else if (select_type == 'product') {
            type_translate = '成品'
        }
        Ewin.confirm({message: '确定撤销&nbsp;&nbsp;' + type_translate + '&nbsp;&nbsp;' + storage_in_id + '&nbsp;&nbsp;' + '入库操作?'}).on(function (e) {
            if (e) {
                $.ajax({
                    'url': '/report/report_storage_in_recover/',
                    'type': 'post',
                    'data': {
                        'storage_in_id': storage_in_id,
                        'select_type': select_type,
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            console.log('撤销成功...');
                            $select_tr.remove();
                        }
                    }
                });
            }
            else {
                window.location.href = '';
            }
        });
    })
});