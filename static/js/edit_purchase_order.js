$(function () {
    var $modify = $('#modify_date');
    var $ord_id = $('#modify_date').attr('name');

    var $date_val = $('#modify_date').attr('date');
    lt = $date_val.split('-');
    if (lt[1].length == 1) {
        lt[1] = '0' + lt[1];
    }
    if (lt[2].length == 1) {
        lt[2] = '0' + lt[2];
    }
    var $date_val = lt[0] + '-' + lt[1] + '-' + lt[2];


    //修改日期
    $('#modify_date').click(function () {
        $(this).parent().replaceWith('<td><input type="date" id="modify" value="' + $date_val + '"></td>');
        document.getElementById('modify').focus();
        $modify = $('#modify');
        $modify.blur(function () {
            window.location.href = '/purchase/edit_pur/?ord_id=' + $ord_id;
        });
        $modify.change(function () {
            var $new_date = $('#modify').val();
            $.ajax({
                'url': '/purchase/edit_pur_date/',
                'type': 'post',
                'data': {
                    'order_id': $ord_id,
                    'new_date': $new_date,
                },
                success: function (res) {
                    if (res.code == 'ok') {
                        window.location.href = '/purchase/edit_pur/?ord_id=' + $ord_id;
                    }
                }
            });
        });
    });


    //导入文件
    document.getElementById('pro_id').focus();
    $('#order_detail').scrollTop(100000);
    $('#file_upload_button').on('click', function () {
        $('#file_in').click();
        $('#file_in').on('change', function () {
            var $form_data = new FormData();
            var $file_info = $('#file_in')[0].files[0];
            $form_data.append('file_in', $file_info);
            $.ajax({
                'url': '/purchase/create_pur_detail/?ord_id=' + $ord_id + '&file_in=True',
                'type': 'post',
                'data': $form_data,
                'processData': false,
                'contentType': false,
                success:
                    function (result) {
                        if (result.code == '888') {
                            var total_count = result.total_count;
                            var total_price = result.total_price;
                            var $title_total_price = $('#pur_order tbody tr td:nth-child(6)');
                            var $total_count = $('#total_count');
                            var old_total_count = $total_count.text();
                            var new_total_count = parseInt(old_total_count) + parseInt(total_count)
                            var $total_price = $("#total_price");
                            for (i of result.file_data) {
                                var pro_id = i.data_pro_id;
                                var pro_count = i.data_pro_count;
                                var pro_type = i.data_pro_type;
                                var pro_unit_price = i.data_pro_unit_price;
                                var pro_price = i.data_pro_price;

                                var $add_data = '<tr class="purchase_detail_"' + pro_id + '>' +
                                    '<td width="10%">' + pro_id + '</td>' +
                                    '<td width="15%">' + pro_type + '</td>' +
                                    '<td width="15%">' + pro_count + '</td>' +
                                    '<td width="15%">' + pro_unit_price + '</td>' +
                                    '<td width="15%">' + pro_price + '</td>' +
                                    '<td width="30%">' +
                                    '<span class="purchase_detail_delete" ord_id="' + $ord_id + '" pro_id="' + pro_id + '" pro_count="' + pro_count + '">删除</span>' +
                                    '</td>' +
                                    '</tr>';
                                $('#pur_order_detail_body tbody').append($add_data);
                            }
                            $total_count.text(new_total_count);
                            $total_price.text(total_price);
                            $title_total_price.text(total_price.toFixed(2));
                            $('#file_in').unbind();

                        }
                        if (result.code == '222') {
                            Ewin.alert({message: '导入文件有误, 请认真核对...'})
                        }
                    }
            });
        });
    });


    //删除
    $('#pur_order_detail_body').on('click', '.purchase_detail_delete', function () {
        var order_id = $(this).attr('ord_id');
        var pro_id = $(this).attr('pro_id');
        var pro_count = $(this).attr('pro_count');
        var $del_colum = $(this).parent().parent();
        var old_price = $(this).parent().prev().text();


        $.ajax({
            'url': '/purchase/del_order_detail/',
            'type': 'post',
            'data': {
                'order_id': order_id,
                'pro_id': pro_id,
                'pro_count': pro_count
            },
            success: function (result) {
                if (result.code == '888') {
                    $del_colum.remove();


                    var $title_total_price = $('#pur_order tbody tr td:nth-child(6)');
                    var $total_count = $('#total_count');
                    var minus_total_count = parseInt($total_count.text()) - parseInt(pro_count);
                    var $total_price = $("#total_price");
                    var minus_total_price = parseFloat($total_price.text()) - parseFloat(old_price);


                    $total_count.text(minus_total_count);
                    $total_price.text(minus_total_price);
                    $title_total_price.text(minus_total_price.toFixed(2));
                    if ($('.purchase_detail_' + pro_id).length < 2) {
                        $('.purchase_detail_' + pro_id).css('color', '');
                    }

                }
            }
        })
    });


    $('#complete').click(function () {
        var predict_freight = $('#predict_freight').val();
        if (!predict_freight) {
            Ewin.alert({message: '请输入运费...'})
        }
        else {
            $.ajax({
                'url': '/purchase/complete_order_detail/',
                'type': 'post',
                'data': {
                    'ord_id': $ord_id,
                    'predict_freight': predict_freight,
                },
                success: function (result) {
                    if (result.code == 'ok') {
                        window.location.href = '/purchase/create_pur/';
                    }
                }

            })
        }
    });


    $('#pro_id').keypress(function (ev) {
        if (ev.charCode == '13' && $(this).val()) {
            $('#pro_count')[0].focus();
        }
    });


    $('#pro_count').keypress(function (ev) {
        if (ev.charCode == '13') {
            if ($(this).val() && $('#pro_id').val()) {
                var $ord_id = $('#pro_id').attr('ord_id');
                var $pro_id = $('#pro_id').val();
                var $pro_count = $('#pro_count').val();
                post_add_product($ord_id, $pro_id, $pro_count);

            }

        }

    });


    $('#pur_submit').on('click', function () {
        if ($('#pro_id').val() && $('#pro_count').val()) {
            var $ord_id = $('#pro_id').attr('ord_id');
            var $pro_id = $('#pro_id').val();
            var $pro_count = $('#pro_count').val();
            post_add_product($ord_id, $pro_id, $pro_count)
        }
    });


    $('#pur_order').on('mouseenter', '#edit_rebate', function () {
        $(this).append('<span id="enter"> 修改</span>')
    });


    $('#pur_order').on('mouseleave', '#edit_rebate', function () {
        $('#enter').remove();
    });


    $('#pur_order').on('click', '#enter', function () {
        var old_rebate = $('#edit_rebate span').eq(0).text();
        var edit_rebate_input = '<input class="form-control" id="rebate_num" type="number" value="' + old_rebate + '" style="margin: 0 auto; ;width: 7rem; height: 1.5rem;">';
        $('#edit_rebate').replaceWith('<td id="edit_rebate_temp"></td>');
        $('#edit_rebate_temp').append(edit_rebate_input);
        $('#rebate_num').select();
        $('#pur_order').on('keypress', '#rebate_num', function (ev) {
            if (ev.charCode == 13) {
                var new_rebate = $(this).val();
                $('#edit_rebate_temp').replaceWith('<td id="edit_rebate"><span class="form-group">' + new_rebate + '</span></td>');
                if (old_rebate !== new_rebate) {
                    var ord_id = $('#pur_order tbody tr td').eq(1).text();
                    $.ajax({
                        'url': '/purchase/edit_pur_rebate/',
                        'type': 'post',
                        'data': {
                            'rebate': new_rebate,
                            'ord_id': ord_id
                        },
                        success: function (result) {
                            if (result.code == '888') {
                            }
                        }
                    })
                }
            }
        });
    });


    $('#pur_order').on('mouseenter', '#handler', function () {
        var $handler_change_button = '<span id="handler_change_button" style="color: #337ab9; cursor: pointer;">&nbsp;&nbsp;修改</span>';
        $(this).append($handler_change_button);
    });

    $('#pur_order').on('mouseleave', '#handler', function () {
        $('#handler_change_button').remove();
    });


    $('#pur_order').on('click', '#handler_change_button', function () {
        var old_handler = $('#handler').children('span').eq(0).text();
        $.ajax({
            'url': '/info/get_user_info/',
            'async': false,
            'type': 'post',
            'data': {
                'get_user_info': 'ok'
            },
            success: function (result) {
                if (result.code == '888') {
                    var $user_option = '';
                    for (i in result['user_info']) {
                        if (result['user_info'][i] == old_handler) {
                            $user_option += '<option selected="selected" value="' + i + '">' + result['user_info'][i] + '</option>'
                        }
                        else {
                            $user_option += '<option value="' + i + '">' + result['user_info'][i] + '</option>'
                        }
                    }
                    var $new_handler_select = '<select id="select_handler" class="form-control">' + $user_option + '</select>';
                    $('#handler').replaceWith('<td id="#handler">' + $new_handler_select + '</td>');
                }
                $('#pur_order').on('change', '#select_handler', function () {
                    var user_id = $(this).prop('selected', true).val();
                    var pur_id = $('#pur_order tbody td').eq(1).text();
                    $.ajax({
                        'url': '/purchase/change_handler/',
                        'async': false,
                        'type': 'post',
                        'data': {
                            'user_id': user_id,
                            'pur_id': pur_id
                        },
                        success: function (result) {
                            if (result.code == '888') {
                                window.location.href = ''
                            }
                        }
                    })
                });


            }
        });
    });


    function post_add_product($ord_id, $pro_id, $pro_count) {
        $.ajax({
            'url': '/purchase/create_pur_detail/?ord_id=' + $ord_id,
            'type': 'post',
            'data': {
                'ord_id': $ord_id,
                'pro_id': $pro_id,
                'pro_count': $pro_count,
            },
            success: function (result) {
                if (result.code == '888') {
                    // window.location.href = '/purchase/edit_pur/?ord_id=' + $ord_id
                    var $title_total_price = $('#pur_order tbody tr td:nth-child(6)');
                    var pro_unit_price = result.pro_unit_price;
                    var $total_count = $('#total_count');
                    var add_total_count = parseInt($total_count.text()) + parseInt($pro_count);
                    var $total_price = $("#total_price");
                    var add_total_price = parseFloat($total_price.text()) + parseInt($pro_count) * pro_unit_price;
                    var $order_detail_tr = '<tr class="purchase_detail_' + $pro_id + '">' +
                        '<td></td>' +
                        '<td width="120px">' + $pro_id + '</td>' +
                        '<td width="120px">' + result.pro_type + '</td>' +
                        '<td width="120px">' + parseInt($pro_count) + '</td>' +
                        '<td width="120px">' + pro_unit_price.toFixed(2) + '</td>' +
                        '<td width="150px">' + (parseInt($pro_count) * pro_unit_price).toFixed(2) + '</td>' +
                        '<td width="120px">' +
                        '<span class="purchase_detail_delete" ord_id="' + $ord_id + '" pro_id="' + $pro_id + '" pro_count="' + $pro_count + '">删除</span>' +
                        '</td>' +
                        '<td></td>' +
                        '</tr>';
                    if (!$('.purchase_detail_' + $pro_id).length) {
                        $('#pur_order_detail_body tbody').append($order_detail_tr);
                    }
                    else {
                        $('#pur_order_detail_body tbody').append($order_detail_tr);
                        $('.purchase_detail_' + $pro_id).css('color', 'red');
                    }
                    $total_count.text(add_total_count);
                    $total_price.text(add_total_price);
                    $title_total_price.text(add_total_price.toFixed(2));
                    $('#pro_id').val('');
                    $('#pro_count').val('');
                    $('#pro_id')[0].focus();
                    $('#order_detail').scrollTop(100000);
                }
                else if (result.code == '000') {
                    Ewin.alert({message: '产品编号不存在...'}).on(function () {
                        $('#pro_id').val('');
                        $('#pro_count').val('');
                        $('#pro_id')[0].focus();
                    })
                }
            }
        });
    }


});