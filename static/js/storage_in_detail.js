$(function () {
    $('#storage_in_detail_body').on('click', '.edit_storage_in_detail', function (e) {
        e.preventDefault();

        // 判断是否已经进入修改状态
        if (!$('#edit_count').length) {
        var old_count = $(this).parents('td').prev().children('span').text();
        $(this).parents('td').prev().children('span').replaceWith('<input type="number" class="form-control" id="edit_count" value="' + old_count + '">');
        $('#edit_count')[0].select();
        $('#storage_in_detail_body').on('keypress', '#edit_count', function (ev) {
            if (ev.charCode == 13) {
                var pro_id = $(this).parent().prev().text();
                var new_count = $(this).val();
                var storage_in_id = $('#storage_in_id').text();
                var storage_in_type = $(this).parents('tbody').attr('storage_in_type');
                var $old_total_count = $('#total_count');

                $.ajax({
                    'url': '/report/report_storage_in_edit/',
                    'type': 'post',
                    'data': {
                        'pro_id': pro_id,
                        'pro_count': new_count,
                        'storage_in_id': storage_in_id,
                        'storage_in_type': storage_in_type
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            $('#edit_count').replaceWith('<span class="pro_count">' + new_count + '</span>');
                            $('#commit_edit').css('display', 'inline');

                            // 更新总数
                            var new_total_count = 0;
                            $('.pro_count').each(function () {
                                console.log($(this).text());
                                new_total_count += parseFloat($(this).text());
                            });
                            $old_total_count.text(new_total_count.toFixed(0));

                        }
                    }
                })
            }
        })
    }
    });

    $('#storage_in_detail_body').on('click', '.del_storage_in_detail', function (e) {
        e.preventDefault();
        var $select_tr = $(this).parents('tr');
        var pro_id = $(this).parents('td').prev().prev().text();
        var new_count = 0;
        var storage_in_id = $('#storage_in_id').text();
        var storage_in_type = $(this).parents('tbody').attr('storage_in_type');
        var $old_total_count = $('#total_count');

        $.ajax({
            'url': '/report/report_storage_in_edit/',
            'type': 'post',
            'data': {
                'pro_id': pro_id,
                'pro_count': new_count,
                'storage_in_id': storage_in_id,
                'storage_in_type': storage_in_type
            },
            success: function (result) {
                if (result.code == '888') {
                    $select_tr.remove();
                    $('#commit_edit').css('display', 'inline');

                    // 更新总数
                    var new_total_count = 0;
                    $('.pro_count').each(function () {
                        console.log($(this).text());
                        new_total_count += parseFloat($(this).text());
                    });
                    $old_total_count.text(new_total_count.toFixed(0));

                }
            }
        });

    });

    $('#close_window').on('click', function () {
        window.close();
    });

    $('#commit_edit').on('click', function () {
        var storage_in_id = $('#storage_in_id').text();
        var storage_in_type = $('#storage_in_detail_body tbody').attr('storage_in_type');
        $.ajax({
            'url': '/report/report_storage_in_confirm/',
            'type': 'post',
            'async': false,
            'data': {
                'confirm': 'ok',
                'storage_in_id': storage_in_id,
                'storage_in_type': storage_in_type
            },
            success: function (result) {
                if (result.code == '888') {
                    var change_detail = result['storage_in_change_'];
                    var show_change_detail = '';
                    for (foo in change_detail) {
                        show_change_detail += '<span>' + foo + '&nbsp;&nbsp;' + change_detail[foo][0] + '&nbsp;&nbsp;->&nbsp;&nbsp;' + change_detail[foo][1] + '</span><br>';
                    }
                    Ewin.confirm({message: show_change_detail + '<br> 确认修改?'}).on(function (e) {
                        if (e) {
                            $.ajax({
                                'url': '/report/report_storage_in_submit/',
                                'type': 'post',
                                'async': false,
                                'data': {
                                    'submit': 'ok',
                                    'storage_in_id': storage_in_id,
                                    'storage_in_type': storage_in_type
                                },
                                success: function (result) {
                                    if (result.code == '888') {
                                        window.location.href = '';
                                    }
                                }
                            });

                        }
                    })
                }
            }
        });

    });

});