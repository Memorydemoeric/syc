$(function () {

    $('#pro_id').focus();

    $('.edit_storage_detail').click(function () {
        var $pro_id = $(this).attr('pro_id');
        var $storage_type = $(this).attr('type');
        var $old_count = $('#' + $pro_id).text();

        if ($storage_type == 'product') {
            type_name = '成品';
        }
        else if ($storage_type == 'half') {
            type_name = '半成品'
        }

        $('#' + $pro_id).replaceWith('<td width="15%">' +
            '<input style="width: 8rem;margin: 0 auto;padding: 0 auto;" id="edit_count" name="count">' +
            '<button style="height: 3rem;margin-left: 1rem;" id="modify_submit" class="btn btn-primary" type="button">提交</button>' +
            '</td>');
        // document.getElementById('edit_count').focus();
        $('#edit_count')[0].focus();

        $('#edit_count').blur(function () {
            if ($('#edit_count').val() == $old_count || !$('#edit_count').val()) {
                window.location.href = ''
            }
        });


        $('#edit_count').keypress(function (ev) {
            if (ev.charCode == 13) {
                $('#edit_count').blur();
                var $new_count = $('#edit_count').val();
                ev.stopPropagation();
                //注册完成按钮的事件
                Ewin.confirm({message: "产品编号：　" + $pro_id + "　　　" + type_name + "</br>" + "数量：　" + $old_count + "　->　" + $new_count}).on(function (e) {
                    if (!e) {
                        window.location.href = ''
                    }
                    else {
                        edit_storage(storage_id = $pro_id, storage_type = $storage_type, storage_count = $new_count)
                    }
                });
            }
        });

        $('#modify_submit').click(function () {
            var $new_count = $('#edit_count').val();
            //注册完成按钮的事件
            Ewin.confirm({message: "产品编号：　" + $pro_id + "　　　" + type_name + "</br>" + "数量：　" + $old_count + "　->　" + $new_count}).on(function (e) {
                if (!e) {
                    window.location.href = ''
                }
                else {
                    edit_storage(storage_id = $pro_id, storage_type = $storage_type, storage_count = $new_count)
                }
            });
        });

    });

    function edit_storage(storage_id, storage_type, storage_count) {
        $.ajax({
            'url': '/storage/alter_storage/',
            'type': 'post',
            'data': {
                'pro_id': storage_id,
                'type': storage_type,
                'count': storage_count,
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/storage/product_storage/'
                }
                else if (result.code == '999') {
                    window.location.href = '/storage/half_storage/'
                }
            },
        })
    }

});