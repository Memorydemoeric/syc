$(function () {

    $('#report_pro_id')[0].focus();

    $('#report_pro_id').on('keypress', function (ev) {
        if (ev.charCode == 13) {
            $('#report_pro_count')[0].focus();

        }
    });

    $('#report_pro_count').on('keypress', function (ev) {
        if (ev.charCode == 13) {
            edit_storage_detail();
        }
    });


    $('#edit_report_storage_out_detail').on('click', function () {
        edit_storage_detail();
    });


    $('#storage_detail').on('click', '.del_storage_detail', function () {
        var pro_id = $(this).parent().attr('pro_id');
        var pur_id = $('#storage_detail').attr('pur_id');
        var $del_storage_detail = $(this);
        $.ajax({
            'url': '/report/edit_report_detail_delete/',
            'type': 'post',
            'data': {
                'pro_id': pro_id,
                'pur_id': pur_id,
            },
            success: function (result) {
                if (result.code == '888') {

                    var pro_count = parseInt($('#pro_id_' + pro_id + ' td')[1].textContent);
                    var pro_price = $('#pro_id_' + pro_id + ' td')[3].textContent;
                    var cust_rebate = result.rebate;

                    var storage_actual_price = parseFloat($('#storage_actual_price').text());
                    var total_count = parseInt($('#total_count').text());
                    var price = parseFloat($('#price').text());


                    total_count -= parseInt(pro_count);
                    price -= parseInt(pro_price);
                    storage_actual_price -= pro_price * parseFloat(cust_rebate) / 100;
                    $del_storage_detail.parent().remove();
                    $('#storage_actual_price').replaceWith('<span id="storage_actual_price">' + storage_actual_price.toFixed(2) + '</span>');
                    $('#total_count').replaceWith('<span id="total_count">' + total_count + '</span>');
                    $('#price').replaceWith('<span id="price">' + price.toFixed(2) + '</span>');
                }
            }
        })
    });


    $('#statement_detail_submit').on('click', function () {
       var pur_id = $('#storage_detail').attr('pur_id');
       var storage_actual_price = $('#storage_actual_price').text();
       var storage_price = $('#price').text();
       Ewin.confirm({message: '确定提交订单？'}).on(function (ev) {
           if (ev) {
               $.ajax({
                   'url': '/report/edit_report_detail_submit/',
                   'type': 'post',
                   'data': {
                       'pur_id': pur_id,
                       'storage_price': storage_price,
                       'storage_actual_price': storage_actual_price,
                   },
                   success: function (result) {
                        if (result.code == '888') {
                            window.close();
                        }
                   }
               })
           }
       })
    });


    function edit_storage_detail() {
        var pur_id = $('#storage_detail').attr('pur_id');
        var report_pro_id = $('#report_pro_id').val();
        var report_pro_count = $('#report_pro_count').val();
        var storage_unit_price, storage_pro_price;
        if (report_pro_id && report_pro_count) {
            $.ajax({
                'url': '/report/edit_report_detail_modify/',
                'type': 'post',
                'data': {
                    'pur_id': pur_id,
                    'pro_id': report_pro_id,
                    'pro_count': report_pro_count,
                },
                success: function (result) {
                    if (result.code != '000') {
                        var storage_actual_price = parseFloat($('#storage_actual_price').text());
                        var total_count = parseInt($('#total_count').text());
                        var price = parseFloat($('#price').text());
                        var cust_rebate = result.cust_rebate;
                        var count_change;
                        storage_unit_price = result.storage_unit_price;
                        storage_pro_price = result.storage_pro_price;
                        var $new_storage_detail = '<tr id="pro_id_' + report_pro_id + '" pro_id="' + report_pro_id + '">\n' +
                            '<th></th>\n' +
                            '<td width="135px">' + report_pro_id + '</td>\n' +
                            '<td width="135px">' + parseInt(report_pro_count).toFixed(0) + '</td>\n' +
                            '<td width="135px">' + parseFloat(storage_unit_price).toFixed(2) + '</td>\n' +
                            '<td width="135px">' + parseFloat(storage_pro_price).toFixed(2) + '</td>\n' +
                            '<td width="100px" class="del_storage_detail">删除</td>\n' +
                            '<th></th>\n' +
                            '</tr>';
                        if (result.code == '999') {
                            $('#storage_detail_body #pro_id_' + report_pro_id).remove();
                            count_change = result.count_change;
                            if (report_pro_count != 0) {
                                $('#storage_detail_body tbody').append($new_storage_detail);
                            }
                        }
                        else if (result.code == '888') {
                            $('#storage_detail_body tbody').append($new_storage_detail);
                            count_change = parseInt(report_pro_count)
                        }
                        $('#storage_detail').scrollTop(100000);
                        total_count += count_change;
                        price += count_change * parseFloat(storage_unit_price);
                        storage_actual_price += count_change * parseFloat(storage_unit_price) * cust_rebate / 100;

                        $('#storage_actual_price').replaceWith('<span id="storage_actual_price">' + storage_actual_price.toFixed(2) + '</span>');
                        $('#total_count').replaceWith('<span id="total_count">' + total_count + '</span>');
                        $('#price').replaceWith('<span id="price">' + price.toFixed(2) + '</span>');

                    }
                    else {
                        Ewin.alert({message: '信息输入有误...'})
                    }
                    $('#report_pro_id').val('');
                    $('#report_pro_count').val('');
                    $('#report_pro_id')[0].focus();
                }
            });
        }
        else {
            $('#report_pro_id').val('');
            $('#report_pro_count').val('');
            $('#report_pro_id')[0].focus();
        }
    }

});