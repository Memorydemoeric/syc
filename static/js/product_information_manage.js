$(function () {
    $('#pro_id').focus();
    $('#pro_id').focus(function () {
        $('#alert_win').css('visibility', 'hidden');
    });
    $('#pro_id').blur(function () {
        $('#alert_win').css('visibility', 'hidden');
    });
    $('#pro_id').keypress(function (ev) {
        if (ev.charCode == '13') {
            var $pro_id = $('#pro_id').val();
            add_product($pro_id);
            edit_func();
        }
    });
    $('#add_product_submit').click(function () {
        var $pro_id = $('#pro_id').val();
        add_product($pro_id);
        edit_func();
    });

    edit_func();


    $('.delete_product_detail').click(function () {
        var $pro_id = $(this).prev().attr('pro_id');
        Ewin.confirm({message: "产品编号：　" + $pro_id + "　确认删除？"}).on(function (e) {
            if (!e) {
            }
            else {
                $.ajax({
                    'url': '/info/delete_product/',
                    'type': 'post',
                    'data': {'pro_id': $pro_id},
                    success: function (result) {
                        if (result.code == '888') {
                            $('#row_' + $pro_id).remove();
                        }
                    }
                })
            }
        });
    });


    $('#input_product').click(function () {
        $('#file_upload').click();
        $('#file_upload').change(function () {
            var $pro_type = $('#input_product').attr('pro_type');
            var $select
            if ($pro_type == 'half') {
                $select = '半成品'
            }
            else if ($pro_type == 'finish') {
                $select = '成品'
            }
            Ewin.confirm({message: "确认要导入 " + $select + " 信息？"}).on(function (e) {
                if (!e) {
                    return;
                }
                else {
                    var $file_name = $('#file_upload').val();
                    var $file_type = $file_name.substr($file_name.length - 4, $file_name.length);
                    var $file_data = new FormData();
                    $file_data.append('excel', $('#file_upload')[0].files[0]);
                    $.ajax({
                        url: '/info/upload_storage_info/?pro_type=' + $pro_type,
                        type: 'POST',
                        async: false,
                        data: $file_data,
                        contentType: false,
                        processData: false,
                        success: function (result) {
                            if (result.code == '888') {
                                Ewin.alert({message: '导入成功...'}).on(function (e) {
                                    if (e) {
                                        window.location.href = '';
                                    }
                                });
                            }
                            else if (result.code == '000') {
                                Ewin.alert({message: '请检查文件内容...'}).on(function (e) {
                                    if (e) {
                                        window.location.href = '';
                                    }
                                });
                            }
                        }
                    })
                }
            });


        })
    });


    function edit_func() {

        $('td').on('click', '.edit_product_detail', function () {
            var $edit_info = {};
            var $new_unit_cost;
            var $new_unit_price;
            var $pro_id = $(this).attr('pro_id');
            var $pro_type = $('.pro_type').first().attr('type');
            var $old_unit_cost = $(this).parent().prev().prev().text();
            var $old_unit_price = $(this).parent().prev().text();
            $(this).parent().prev().prev().replaceWith('<td width="15%">' +
                '<input style="width: 8rem;margin: 0 auto;padding: 0 auto;" id="edit_cost" name="unit_cost">' +
                '<button style="height: 3rem;margin-left: 1rem;" id="modify_submit" class="btn btn-primary" type="button">提交</button>' +
                '</td>');
            $('#edit_cost')[0].focus();


            $('#edit_cost').keypress(function (ev) {
                if (ev.charCode == '13') {
                    $new_unit_cost = $('#edit_cost').val();
                    if ($new_unit_cost) {
                        $edit_info['new_unit_cost'] = $new_unit_cost;
                        $('#edit_cost')[0].blur();
                    }
                    else {
                        $new_unit_cost = $old_unit_cost;
                        $('#edit_cost')[0].blur();
                    }
                }
            });

            $('#edit_cost').blur(function () {

                if (!$new_unit_cost && !$('#edit_cost').val()) {
                    $new_unit_cost = $old_unit_cost;
                }
                else if (!$new_unit_cost && $('#edit_cost').val()) {
                    $new_unit_cost = $('#edit_cost').val();
                    $edit_info['new_unit_cost'] = $('#edit_cost').val();
                }
                $(this).parent().next().replaceWith('<td width="15%">' +
                    '<input style="width: 8rem;margin: 0 auto;padding: 0 auto;" id="edit_price" name="unit_price">' +
                    '<button style="height: 3rem;margin-left: 1rem;" id="modify_submit" class="btn btn-primary" type="button">提交</button>' +
                    '</td>');
                $('#edit_price')[0].focus();
                $(this).parent().replaceWith('<td width="20%">' + parseFloat($new_unit_cost).toFixed(2) + '</td>');

                $('#edit_price').keypress(function (ev) {
                    if (ev.charCode == '13') {
                        $new_unit_price = $('#edit_price').val();
                        if ($new_unit_price) {
                            $edit_info['new_unit_price'] = $new_unit_price;
                            $('#edit_price')[0].blur();
                        }
                        else {
                            $new_unit_price = $old_unit_price;
                            $('#edit_price')[0].blur();
                        }
                    }
                });


                $('#edit_price').blur(function () {


                    if (!$new_unit_price && !$('#edit_price').val()) {
                        $new_unit_price = $old_unit_price;
                    }
                    else if (!$new_unit_price && $('#edit_price').val()) {
                        $new_unit_price = $('#edit_price').val();
                        $edit_info['new_unit_price'] = $('#edit_price').val();
                    }

                    $(this).parent().replaceWith('<td width="20%">' + parseFloat($new_unit_price).toFixed(2) + '</td>');

                    if ($edit_info.new_unit_price || $edit_info.new_unit_cost) {
                        Ewin.confirm({message: "产品编号：　" + $pro_id + "　　　" + $('.pro_type').first().text() + "</br>" + "成本价：　" + $old_unit_cost + "　->　" + parseFloat($new_unit_cost).toFixed(2) + "</br>" + "标准零售价：　" + $old_unit_price + "　->　" + parseFloat($new_unit_price).toFixed(2)}).on(function (e) {
                            if (!e) {
                                $('[pro_id="' + $pro_id + '"]').parent().prev().prev().replaceWith('<td width="20%">' + parseFloat($old_unit_cost).toFixed(2) + '</td>')
                                $('[pro_id="' + $pro_id + '"]').parent().prev().replaceWith('<td width="20%">' + parseFloat($old_unit_price).toFixed(2) + '</td>')
                            }
                            else {
                                $.ajax({
                                    'url': '/info/edit_product/',
                                    'type': 'post',
                                    'data': {
                                        'pro_id': $pro_id,
                                        'type': $pro_type,
                                        'pro_info': $edit_info,
                                    },
                                    success: function (result) {
                                        if (result.code == '888') {
                                        }
                                    }
                                })
                            }
                        });
                    }


                })


            });

        });


    };


    function add_product(pro_id) {
        $.ajax({
            'url': '/info/add_product/',
            'type': 'post',
            async: false,
            'data': {
                'pro_id': pro_id,
            },
            success: function (result) {
                if (result.code == '888') {
                    $('#pro_id').val('');
                    $('#product_detail').scrollTop(100000);
                    $('#product_info').append('<tr style="color: red;">\n' +
                        '                        <td width="15%">' + pro_id + '</td>\n' +
                        '                        <td width="20%">' + $(".pro_type").first().text() + '</td>\n' +
                        '                        <td width="20%">0.00</td>\n' +
                        '                        <td width="20%">0.00</td>\n' +
                        '                        <td width="25%"><span pro_id="' + pro_id + '" class="edit_product_detail"\n' +
                        '                        >修改</span>&nbsp;&nbsp;<span style="color: #000;">|</span>&nbsp;&nbsp;<span class="delete_product_detail">删除</span>\n' +
                        '                        </td>\n' +
                        '                    </tr>');
                }
                else {
                    $('#alert_win').css('visibility', 'visible');
                }
            },
        })
    }

});