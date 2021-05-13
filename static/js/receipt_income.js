$(function () {
    $('#income')[0].focus();

    $('input:checkbox').on('change', function () {
            var total_count = 0;
            var total_actual_price = 0;
            var $checked_pur = $('input:checked');
            var reg = /[\d\.]+/g;
            var str_total_actual_price = $(this).parent().next().next().next().text();
            var reg_list = str_total_actual_price.match(reg);
            $checked_pur.each(function () {
                total_count += parseInt($(this).parent().next().next().text());
                total_actual_price += (Math.round(reg_list[0]) + Math.round(reg_list[1]));
            });
            $('#total_count').text(total_count);
            $('#total_actual_price').text(total_actual_price.toFixed(2));
        }
    );


    $('input:checkbox').on('click', function () {
        var check_statement = $(this).prop('checked');
        $('input:checked').prop('checked', false);
        if (check_statement) {
            $(this).prop('checked', true);
        }
    });


    $('#receipt_submit').on('click', function () {
        var cust_id = $('#income').attr('cust_id');
        var income_account = $('#income').val();
        if (income_account) {
            var $pur_select = $('input:checked').length;

            if (!$pur_select) {
                Ewin.alert({message: '请选择订单!'}).on(function (ev) {

                });
            }


            else {

                Ewin.confirm({message: '确认提交金额？'}).on(function (ev) {
                    if (ev) {
                        var pur_id_list = new Array();
                        $('input:checked').each(function () {
                            pur_id_list.push($(this).parent().attr('pur_id'));
                        });
                        $.ajax({
                            'url': '/purchase/receipt_income_submit/',
                            'type': 'post',
                            'datatype': 'JSON',
                            'data': {
                                'pur_id': pur_id_list,
                                'cust_id': cust_id,
                                'account': income_account,
                            },
                            success: function (result) {
                                if (result.code == '888') {
                                    window.location.href = '/purchase/receipt/'
                                }
                            }
                        })
                    }
                });
            }
        }
    });


    $('#income').on('keypress', function (e) {
        if (e.charCode == 13) {
            e.preventDefault();
            var $pur_select = $('input:checked').length;

            if (!$pur_select) {
                Ewin.alert({message: '请选择订单!'}).on(function (ev) {

                });
            }
            else {
                var cust_id = $('#income').attr('cust_id');
                var income_account = $('#income').val();
                if (income_account) {
                    Ewin.confirm({message: '确认提交金额？'}).on(function (ev) {
                            if (ev) {
                                var pur_id_list = new Array();
                                $('input:checked').each(function () {
                                    pur_id_list.push($(this).parent().attr('pur_id'));
                                });
                                $.ajax({
                                    'url': '/purchase/receipt_income_submit/',
                                    'type': 'post',
                                    'datatype': 'JSON',
                                    'data': {
                                        'pur_id': pur_id_list,
                                        'cust_id': cust_id,
                                        'account': income_account,
                                    },
                                    success: function (result) {
                                        if (result.code == '888') {
                                            window.location.href = '/purchase/receipt/'
                                        }
                                    }
                                })
                            }
                        }
                    );
                }
            }

        }
    });
});