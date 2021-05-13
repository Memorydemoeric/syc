$(function () {
    $('#pro_id')[0].focus();

    $('#pro_id').keypress(function (ev) {
        if (ev.charCode == 13) {
            $('#pro_count')[0].focus();
        }
    });


    $('.storage_in_modify').on('click', '.storage_in_detail_line', function () {
        if ($(this).hasClass('tr_selected')) {
            $(this).removeClass('tr_selected')
        }
        else {
            $('.tr_selected').removeClass('tr_selected');
            $(this).addClass('tr_selected');
        }
    });


    $('#storage_in_upload').on('click', function () {
        $('#file_upload').click();
        $('#file_upload').on('change', function () {
            var $form_data = new FormData();
            var $file_info = $('#file_upload')[0].files[0];
            $form_data.append('file_info', $file_info);
            $.ajax({
                'url': '/storage/half_storage_in_upload/',
                'type': 'post',
                'data': $form_data,
                'processData': false,
                'contentType': false,
                success: function (result) {
                    if (result.code == '888') {
                        window.location.href = '/storage/half_storage_in/'
                    }
                }
            })
        })
    });


    $('#pro_count').keypress(function (ev) {
        if (ev.charCode == 13 && $('#pro_id').val() && $('#pro_count').val()) {
            var $data = {
                'pro_id': $('#pro_id').val(),
                'pro_count': $('#pro_count').val(),
            };
            storage_in_add(url = '/storage/half_storage_in_add/', data = $data)
        }
        else if (ev.charCode == 13 && (!$('#pro_id').val() || !$('#pro_count').val())) {
            $('#pro_id').val('');
            $('#pro_count').val('');
            $('#pro_id')[0].focus();
        }
    });


    $('#storage_in_submit').click(function () {
        var $data = {
            'pro_id': $('#pro_id').val(),
            'pro_count': $('#pro_count').val(),
        };
        storage_in_add(url = '/storage/half_storage_in_add/', data = $data)
    });


    $('#clear_storage_in').click(function () {
        Ewin.confirm({message: "是否清空列表？"}).on(function (e) {
            if (!e) {
            }
            else {
                $.ajax({
                    'url': '/storage/half_storage_in_clear/',
                    'type': 'post',
                    'data': {
                        'order': 'clear_list',
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            window.location.href = '/storage/half_storage_in/'
                        }
                    }
                })
            }
        });
    });


    $('.storage_in_modify').on('click', '.modify_count', function () {
        var $pro_id = $(this).parent().attr('pro_id');
        var $old_count = parseInt($(this).parent().prev().text());
        $(this).parent().prev().replaceWith('<td width="15%">' +
            '<input type="number" style="width: 8rem;margin: 0 auto;padding: 0 auto;" id="edit_count_' + $pro_id + '" name="count"></td>');
        $('#edit_count_' + $pro_id)[0].focus();
        $('.storage_in_modify').on('keypress', '#edit_count_' + $pro_id, function (ev) {
            if (ev.charCode == 13) {
                if ($('#edit_count_' + $pro_id).val() && ($('#edit_count').val() !== $old_count)) {
                    var $data = {
                        'pro_id': $pro_id,
                        'pro_count': $('#edit_count_' + $pro_id).val(),
                    };
                    modify_storage_count('/storage/half_storage_in_detail_modify/', $data);
                    $old_count = $('#edit_count_' + $pro_id).val();
                }
                else {
                    $('#edit_count_' + $pro_id).parent().replaceWith('<td class="storage_pro_count" width="30%">' + $old_count + '</td>');

                }
            }
        });

        $('.storage_in_modify').on('blur', '#edit_count_' + $pro_id, function () {
            if (!$('#edit_count_' + $pro_id).val()) {
                $('#edit_count_' + $pro_id).parent().replaceWith('<td class="storage_pro_count" width="30%">' + $old_count + '</td>');
            }
        });

    });


    $('.storage_in_modify').on('click', '.del_pro', function () {
        var $pro_id = $(this).parent().attr('pro_id');
        var $data = {
            'pro_id': $pro_id,
        };
        del_storage_pro('/storage/half_storage_in_detail_del/', $data);
    });


    $('#submit_storage_in').click(function () {
        window.location.href = '/storage/half_storage_in_confirm/'
    });


    function del_storage_pro(url, data) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': data,
            success: function (result) {
                if (result.code == '888') {
                    $('#line_pro_id_' + data.pro_id).remove();
                    var sum = flush_total_count();
                    $('#total_count').text(sum);
                }
            }
        });
    }


    function modify_storage_count(url, data) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': data,
            success: function (result) {
                if (result.code == '888') {
                    $('#edit_count_' + data.pro_id).parent().replaceWith('<td class="storage_pro_count" width="30%">' + data.pro_count + '</td>');
                    var sum = flush_total_count();
                    $('#total_count').text(sum);
                }
            }
        });
    }

    function flush_total_count() {
        var $counts = $('.storage_pro_count');
        var sum = 0;
        for (i = 0; i < $counts.length; i++) {
            sum += parseInt($counts[i].textContent);
        }
        return sum
    }


    function storage_in_add(url, data) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': data,
            success: function (result) {
                if (result.code == '888' || result.code == '000') {
                    if (result.code == '000') {
                        $('#line_pro_id_' + data.pro_id).remove();
                    }
                    var $append_product = '<tr id="line_pro_id_' + data.pro_id + '" class="storage_in_detail_line">' +
                        '<td width="30%"  style="text-align: right">' + data.pro_id + '&nbsp;&nbsp;&nbsp;&nbsp;</td>' +
                        '<td width="30%" class="storage_pro_count">' + data.pro_count + '</td>' +
                        '<td width="40%" class="storage_in_modify" pro_id="' + data.pro_id + '" pro_count="' + data.pro_count + '">' +
                        '<span class="modify_count">修改</span>&nbsp;&nbsp;|&nbsp;&nbsp;<span class="del_pro">删除</span></td></tr>';
                    $('#storage_in_body tbody').append($append_product);
                    $('#storage_in_detail').scrollTop(100000);
                    $('#pro_id').val('');
                    $('#pro_count').val('');
                    $('#pro_id')[0].focus();
                    var sum = flush_total_count();
                    $('#total_count').text(sum);
                }
                else {
                    $('#pro_id').val('');
                    $('#pro_count').val('');
                    $('#pro_id')[0].focus();
                }
            }
        })
    }


})
;