$(function () {

    var pur_id;
    var old_cash;

    var $cash_change = $('.abs_cash_change');
    $cash_change.each(function () {
        var cash_change = $(this).text();
        cash_change = cash_change.replace('-', '');
        $(this).text('+ ' + cash_change);
    });

    var $minus_change = $('.minus_change');
    $minus_change.each(function () {
        var minus_change = $(this).text();
        minus_change = minus_change.replace('-', '');
        $(this).text('- ' + minus_change);
    });


    $('#storage_detail_body').on('mouseenter', '.income', function () {
        var $change_income = '<span pro_id="" id="change_income">&nbsp;&nbsp;修改</span>';
        $(this).append($change_income);
    });

    $('#storage_detail_body').on('mouseleave', '.income', function () {
        $('#change_income').remove();
    });

    $('#storage_detail_body').on('click', '#change_income', function () {
        old_cash = $(this).parent().text().split('+')[1].split('  ')[0].split(' ')[1];
        pur_id = $(this).parent().attr('pur_id');
        console.log('old_cash:', old_cash);
        $(this).parent().replaceWith('<td width="15%"><input class="form-control" type="number" id="change_income_input" value="' + old_cash + '"></td>');
        $('#change_income_input')[0].select();
    });

    $('#storage_detail_body').on('keypress', '#change_income_input', function (ev) {
        if (ev.charCode == 13) {
            var new_cash = $(this).val();
            Ewin.confirm({message: '修改收款金额：' + old_cash + '  ->  ' + new_cash}).on(function (e) {
                if (e) {
                    $.ajax({
                        'url': '/report/report_change_income/',
                        'type': 'post',
                        'data': {
                            'pur_id': pur_id,
                            'new_income': $('#change_income_input').val()
                        },
                        success: function (result) {
                            if (result.code == '888') {
                                window.location.href = '/report/statement_detail/?cust_id=' + result.cust_id;
                            }
                        }
                    });
                }
                else {
                    window.location.href = ''
                }
            });
        }
    })


});