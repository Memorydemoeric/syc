$(function () {
    $('#location')[0].focus();
    $('#location').on('keyup', function () {
        var location = $('#location').val();
        $.ajax({
            'url': '/purchase/refund_select/',
            'type': 'post',
            'data': {
                'location': location
            },
            success: function (result) {
                if (result.code == '888') {
                    $('#customer').children().remove();
                    var cust_info = result['cust_info'];
                    for (foo in cust_info) {
                        var $cust_option = '<option value="' + cust_info[foo] + '">' + foo + '</option>';
                        $('#customer').append($cust_option);
                    }
                }
            }
        })
    });


    $('#submit_refund_purchase').click(function () {
        var $cust_id = $('#customer').val();
        window.location.href = '/purchase/refund_purchase_detail/?cust_id=' + $cust_id;
    });
});