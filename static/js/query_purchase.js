$(function () {
    // var ord_id = null;
    var total_count = 0;
    var total_price = 0;
    var body_scroll = $('#body_scroll').val();
    var pur_num = $('#pur_order_foot tr').length;
    $('#total_pur_num').text(pur_num);


    var select_num = $('input[status="True"]').length;
    $('#select_pur_num').text(select_num);


    var caculate = function () {
        $('.pur_select[status="True"]').each(function () {
            var pro_price = $(this).parent().siblings('.pro_price').children('span').text();
            var pro_count = $(this).parent().siblings('.pro_count').children('span').text();
            total_price += parseFloat(pro_price);
            total_count += parseInt(pro_count)
        });

        $('#total_count').text(total_count);
        $('#total_price').text(total_price);
    };

    caculate();


    $.ajax({
        'url': '/purchase/select_detail/',
        'type': 'post',
        'dataType': 'JSON',
        'data': {'check': 'show_select_detail'},
        success: function (result) {
            if (result.code == '888') {
                $('#pur_order_detail_body tr').each(function () {
                    var pro_id = $(this).attr('id').split('_')[2];
                    $(this).attr('title', result.pur_detail[pro_id]);
                });
            }
        }
    });


    $('#order_body').scrollTop(body_scroll);

    $('input[status="True"]').prop('checked', 'checked');
    if ($('input[status="True"]').length == $('input[status]').length) {
        $('#all_select').prop('checked', true);
    }
    else {
        $('#all_select').prop('checked', false);
    }
    $('#all_select').change(function () {
        $.ajax({
            'url': '/purchase/select_purchase/',
            'type': 'post',
            'data': {
                'all_select': Number($(this).prop('checked'))
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/purchase/query_purchase/'
                }
            }
        })
    });


    $('input[status]').change(function () {
        var body_scroll = $('#order_body').scrollTop();
        $.ajax({
            'url': '/purchase/select_purchase/',
            'type': 'post',
            'data': {
                'id': Number($(this).attr('id')),
                'status': Number($(this).prop('checked')),
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/purchase/query_purchase/?body_scroll=' + body_scroll
                }
            }
        });

    });

    $('#produce_report').click(function () {
        var arr1 = [];
        $('input[status="True"]').each(function () {
            arr1.push($(this).attr('id'));
        });
        $.ajax({
            'url': '/plan/create_plan/',
            'type': 'post',
            'data': {
                'order_id': arr1
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/plan/create_plan/'
                }
            },
        })
    });


    $(".modify_date").click(function () {
        var $date = $(this).attr('date');
        lt = $date.split('-');
        if (lt[1].length == 1) {
            lt[1] = '0' + lt[1];
        }
        if (lt[2].length == 1) {
            lt[2] = '0' + lt[2];
        }
        var $date_val = lt[0] + '-' + lt[1] + '-' + lt[2];
        var ord_id = $(this).attr('ord_id');
        $(this).parent().replaceWith('<td><input type="date" id="modify" value="' + $date_val + '"></td>');

        document.getElementById('modify').focus();
        var $modify = $('#modify');

        $modify.blur(function () {
            var $new_date = $modify.val();
            $.ajax({
                'url': '/purchase/query_purchase/modify_date/',
                'type': 'post',
                'data': {
                    'ord_id': ord_id,
                    'new_date': $new_date,

                },
                success: function (result) {
                    if (result.code == '888') {
                        window.location.href = '/purchase/query_purchase/';
                    }
                }
            })
        });
    });


    $('#product_out').click(function () {
        var arr2 = [];
        $('input[status="True"]').each(function () {
            arr2.push($(this).attr('id'));
        });


        $.ajax({
            'url': '/storage/storage_outing/',
            'type': 'post',
            'data': {
                'order_id': arr2
            },
            success: function (result) {
                if (result.code == '888') {
                    window.location.href = '/storage/product_storage_out/'
                }
            },
        })
    });


});