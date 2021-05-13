$(function () {
    var page_scroll = 0;
    page_scroll = parseInt($('#page_scroll').val());
    $('#order_detail').scrollTop(page_scroll);


    if ($('.storage_out').length == $('.glyphicon-ok').length && $('.storage_out').length != 0) {
        Ewin.confirm({
            message: "确定出库操作？"
        }).on(function (e) {
            if (!e) {
            }
            else {
                $.ajax({
                    'url': '/storage/storage_out_commit/',
                    'type': 'post',
                    'data': {
                        'order': 'storage_out_commit'
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            Ewin.alert({message: '出库成功...'}).on(function () {
                                window.location.href = '/storage/'
                            });
                        }
                    }
                })
            }
        });
    }


    $('.modify_count').click(function () {
        var $ord_id = $(this).attr('ord_id');
        var $pro_id = $(this).attr('pro_id');
        var $old_count = $(this).attr('pro_count');
        $(this).parent().siblings('.pro_count').replaceWith('<td width="15%">' +
            '<input style="width: 8rem;margin: 0 auto;padding: 0 auto;" id="edit_count" name="count">' +
            '<button style="height: 3rem;margin-left: 1rem;" id="modify_submit" class="btn btn-primary" type="button">提交</button>' +
            '</td>');
        $('#edit_count')[0].focus();
        $('#edit_count').blur(function () {
            if ($('#edit_count').val() == $old_count || !$('#edit_count').val()) {
                window.location.href = ''
            }
        });

        $('#modify_submit').click(function () {
            var $new_count = $('#edit_count').val();
            out_ajax('/storage/product_storage_out_edit/', $ord_id, $pro_id, $new_count, null, page_scroll)
        });

        $('#edit_count').keypress(function (ev) {
            if (ev.charCode == '13') {
                var $new_count = $('#edit_count').val();
                out_ajax(url = '/storage/product_storage_out_edit/', ord_id = $ord_id, pro_id = $pro_id, pro_count = $new_count,null, page_scroll)
            }
        })
    });


    $('.del_element').click(function () {
        var $ord_id = $(this).attr('ord_id');
        var $pro_id = $(this).attr('pro_id');
        out_ajax('/storage/product_storage_out_del/', $ord_id, $pro_id, null, null, page_scroll)
    });


    $('#order_detail').on('scroll', function () {
        page_scroll = $(this).scrollTop();
    });


    $('#storage_out_report').click(function () {
        var $ord_id = $(this).attr('ord_id');
        var $handler = $('#handler option:selected').val();
        if ($('#translation_expense').val()) {
            storage_out_submit('/storage/product_storage_out_submit/', $ord_id, $('#translation_expense').val(), $handler, page_scroll)
        }
        else {
            Ewin.alert({message: '请输入运费'})
        }
    });


    $('#storage_out_list_output').click(function () {
        var $purchase_id = $(this).attr('ord_id');
        $.ajax({
            'url': '/storage/storage_out_list_output/',
            'type': 'post',
            'data': {
                'ord_id': $purchase_id,
            },
            success: function (result) {
                if (result.code == '888') {
                    var $file_name = result.file_name;
                    $('#storage_output').attr('href', '/storage/storage_output_download/?file_name=' + $file_name);
                    document.getElementById("storage_output").click();
                }
            }
        })
    });


    $('#storage_out_reset').on('click', function () {
       var order_id = $(this).attr('ord_id');
        $.ajax({
            'url': '/storage/product_storage_out_reset/',
            'type': 'post',
            'data': {
                'order_id': order_id
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = ''
                }
            }
        })
    });


    function out_ajax(url, ord_id, pro_id = null, pro_count = null, pur_handler, scroll) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': {
                'ord_id': ord_id,
                'pro_id': pro_id,
                'pro_count': pro_count,
                'pur_handler': pur_handler,
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/storage/product_storage_out/?ord_id=' + ord_id + '&scroll=' + scroll
                }
            }
        })
    }


    function storage_out_submit(url, ord_id, translation_expense, pur_handler, scroll) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': {
                'ord_id': ord_id,
                'translation_expense': translation_expense,
                'pur_handler': pur_handler,
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/storage/product_storage_out/?ord_id=' + ord_id + '&scroll=' + scroll
                }
            }
        })
    }

});