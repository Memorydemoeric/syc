$(function () {
    $('#pro_id')[0].focus();
    $('#pro_id').keypress(function (ev) {
        if (ev.charCode == 13) {
            $('#pro_count')[0].focus();
            $('#pro_count').keypress(function (ev) {
                if (ev.charCode == 13) {
                    var $pro_id = $('#pro_id').val();
                    var $pro_count = $('#pro_count').val();
                    $.ajax({
                        'url': '/purchase/refund_purchase_detail_add/',
                        'type': 'post',
                        'data': {
                            'pro_id': $pro_id,
                            'pro_count': $pro_count,
                        },
                        success: function (result) {
                            if (result.code == '888') {
                                window.location.href = ''
                            }
                        }
                    });
                }
            })
        }
    });

    $('#add_refund').click(function () {
        var $pro_id = $('#pro_id').val();
        var $pro_count = $('#pro_count').val();
        $.ajax({
            'url': '/purchase/refund_purchase_detail_add/',
            'type': 'post',
            'data': {
                'pro_id': $pro_id,
                'pro_count': $pro_count,
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = ''
                }
            }
        });
    });

    $('.del_refund').click(function () {
        var $pro_id = $(this).attr('pro_id');
        $.ajax({
            'url': '/purchase/refund_purchase_detail_delete/',
            'type': 'post',
            'data': {
                'pro_id': $pro_id,
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = ''
                }
            }
        })
    });

    $('#submit_refund').click(function () {
        var $cust_id = $('#cust_info').attr('cust_id');
        Ewin.confirm({message: '确定提交退货单？'}).on(function (e) {
            if (!e) {
                window.location.href = ''
            }
            else {
                $.ajax({
                    'url': '/purchase/refund_purchase_detail_submit/',
                    'type': 'post',
                    'data': {
                        'code': 'submit_refund',
                        'cust_id': $cust_id,
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            Ewin.alert({message: '退货成功...'}).on(function () {
                                window.location.href = '/purchase/'
                            });

                        }
                    }

                })
            }
        })
    })


});