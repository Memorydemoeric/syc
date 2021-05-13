$(function () {
    $('#cust_condition')[0].focus();

    $('#cust_condition').on('change keypress', function (ev) {
        if (ev.charCode == 13) {
            ev.preventDefault();
        }
        var location = $(this).val();
        $.ajax({
            'url': '/report/statement_select_location/',
            'type': 'post',
            'data': {
                'location': location
            },
            success: function (result) {
                if (result.code == '888') {
                    var cust_info = result.cust_info;
                    $('#cust_info>option').remove();
                    for (var i of cust_info) {
                        var $option = '<option value="' + i.id + '">' + i.cust_name + '</option>';
                        $('#cust_info').append($option);
                    }
                }
            }
        })
    });

    $('.cust_rank').on('click', function (e) {
        var cust_id = $(this).attr('cust_id');
        window.location.href = '/report/statement_detail/?cust_id=' + cust_id;
    });

    $('#cust_id_submit').on('click', function () {
        var cust_id = $(this).prev().val();
        window.location.href = '/report/statement_detail/?cust_id=' + cust_id;
    });


});