$(function () {
    $('#location').on('keyup', function () {
        $.ajax({
            url: '/purchase/show_pur/',
            type: 'post',
            data: {
                'location': $('#location').val(),
            },
            success: function (result) {
                $('#cust_name option').remove();
                for (i of result.cust_info) {
                    $('#cust_name').append('<option name="' + i.id + '">' + i.name + '</option>')
                }
                var $cust_id = $('#cust_name option:selected').attr('name');
                $('#secret_cust_id').val($cust_id);
            },
        })
    });


    $('#cust_name').change(function () {
        var $cust_id = $('#cust_name option:selected').attr('name');
        $('#secret_cust_id').val($cust_id);
    });


    //注册删除按钮的事件
    $(".del_order").click(function () {
        var $order_id = $(this).attr('name');
        var $id = $(this).attr('order_id');
        Ewin.confirm({message: "确认要删除 订单" + $id + " 吗？"}).on(function (e) {
            if (!e) {
                return;
            }
            $.ajax({
                'url': '/purchase/delete_pur/',
                'type': 'post',
                'data': {'id': $order_id},
                success: function (res) {
                    if (res.code == 'ok') {

                        $('tr[name=' + $order_id + ']').remove()
                    }
                }
            })
        });
    });


    //注册完成按钮的事件
    $(".comment_order").click(function () {
        var $order_id = $(this).attr('name');
        var $id = $(this).attr('order_id');
        $('#comment_' + $id).replaceWith('<input type="text" id="comment_input" style="width: 10rem; padding: 0; margin: 0;">');
        $('#comment_input')[0].focus();
        $('#comment_input').blur(function () {
            var comment = $(this).val();
            uploadComment($id, comment)
        });

        $('#comment_input').keypress(function (ev) {
            if (ev.charCode == 13) {
                var comment = $(this).val();
                uploadComment($id, comment)
            }
        });


    });


    function uploadComment(ord_id, comment) {
        $.ajax({
            'url': '/purchase/comment_pur/',
            'type': 'post',
            'data': {
                'order_id': ord_id,
                'comment': comment,
            },
            success: function (res) {
                if (res.code == 'ok') {
                    window.location.href = ''
                }
            }
        })
    }


});


