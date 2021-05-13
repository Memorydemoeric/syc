$(function () {

    $('#search_customer_input')[0].focus();

    $('#search_customer_submit').on('click', function () {
        var condition = $('#search_customer_input').val();
        window.location.href = '/system/show_original_balance/?cust_condition=' + condition;
    });

    $('#search_customer_input').on('keypress', function (ev) {
        if (ev.charCode == 13) {
            var condition = $('#search_customer_input').val();
            window.location.href = '/system/show_original_balance/?cust_condition=' + condition;
        }
    });

    $('.change_balance').on('mouseenter', function () {
        $(this).append('<span class="change_button">&nbsp;&nbsp;&nbsp;&nbsp;修改</span>');
    });

    $('#cust_rank_body').on('mouseleave', '.change_balance', function () {
        $('.change_button').remove();
    });

    $('#cust_rank_body').on('click', '.change_button', function () {
        var old_balance = $(this).prev().text();
        $('.change_button').unbind();
        $(this).parent().replaceWith('<td width="120px" class="change_balance"><input id="change_balance_input" class="form-control" style="height: 2rem;"></td>');
        $('#change_balance_input')[0].focus();
        $('#cust_rank_body').on('keypress', '#change_balance_input', function (ev) {
            if (ev.charCode == 13) {
                var new_balance = $('#change_balance_input').val();
                Ewin.confirm({message: '确定修改余额:&nbsp;&nbsp;' + old_balance + '&nbsp;&nbsp;&nbsp;&nbsp;->&nbsp;&nbsp;&nbsp;&nbsp;' + parseFloat(new_balance).toFixed(1)}).on(function (e) {
                    if (e) {
                        var cust_id = $('#change_balance_input').parent().parent().attr('cust_id');
                        $.ajax({
                            'url': '/system/change_original_balance/',
                            'type': 'post',
                            'data': {
                                'new_balance': new_balance,
                                'cust_id': cust_id
                            },
                            success: function (result) {
                                if (result.code == '888') {
                                    window.location.href = ''
                                }
                            }
                        })
                    }
                    else {
                        window.location.href = ''
                    }
                })

            }
        })

    });

});