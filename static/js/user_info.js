$(function () {
    $('#user_name')[0].focus();


    $('#user_name').on('keypress', function (ev) {
        if (ev.charCode == 13 && $(this).val()) {
            var user_name = $(this).val();
            post_user_name(user_name);
        }
    });


    $('#user_add_submit').on('click', function () {
        if ($(this).prev().val()) {
            var user_name = $(this).prev().val();
            post_user_name(user_name);
        }
    });


    $('#user_info_table_body').on('click', '.del_user_info', function () {
        var user_id = $(this).attr('user_id');
        var $del_tr = $(this);
        var user_name = $(this).parent().prev().prev().prev().text();
        Ewin.confirm({message: '确认删除用户 <b style="color: red">' + user_name + '</b>?'}).on(function (ev) {
            if (ev) {
                $.ajax({
                    'url': '/info/del_user_info/',
                    'type': 'post',
                    'data': {
                        'user_id': user_id
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            $del_tr.parents('tr').remove();
                        }
                    }
                });
            }
        });
    });


    $('#user_info_table_body').on('click', '.change_user_info', function () {
        var $this_tr = $(this).parents('tr');
        var $user_name = $this_tr.children().eq(2).children();
        var $user_telephone_number = $this_tr.children().eq(3).children();
        var $user_comment = $this_tr.children().eq(4).children();
        var user_id = $(this).attr('user_id');
        $user_name.replaceWith('<input class="form-control" style="width: 10rem; height: 2rem; margin: 0 auto;" type="text" id="change_user_name" value="' + $user_name.text() + '">');
        $('#change_user_name')[0].select();
        $('#user_info_table_body').on('keypress', '#change_user_name', function (ev) {
            if (ev.charCode == 13) {
                var new_user_name = $('#change_user_name').val();
                $('#change_user_name').replaceWith('<span>' + new_user_name + '</span>');
                $('#change_user_name').remove();
                $user_telephone_number.replaceWith('<input class="form-control" style="width: 15rem; height: 2rem; margin: 0 auto;" type="text" id="change_user_telephone_number" value="' + $user_telephone_number.text() + '">');
                $('#change_user_telephone_number')[0].select();
                $('#user_info_table_body').on('keypress', '#change_user_telephone_number', function (ev) {
                    if (ev.charCode == 13) {
                        var new_user_telephone_number = $('#change_user_telephone_number').val();
                        $('#change_user_telephone_number').replaceWith('<span>' + new_user_telephone_number + '</span>');
                        $user_comment.replaceWith('<input class="form-control" style="width: 15rem; height: 2rem; margin: 0 auto;" type="text" id="change_user_comment" value="' + $user_comment.text() + '">');
                        $('#change_user_comment')[0].select();
                        $('#user_info_table_body').on('keypress', '#change_user_comment', function (ev) {
                            if (ev.charCode == 13) {
                                var new_user_comment = $('#change_user_comment').val();
                                $('#change_user_comment').replaceWith('<span>' + new_user_comment + '</span>');
                                Ewin.confirm({message: '确认修改？'}).on(function (ev) {
                                    if (!ev) {
                                        window.location.href = '';
                                    }
                                    else {
                                        $.ajax({
                                            'url': '/info/change_user_info/',
                                            'type': 'post',
                                            'datatype': 'JSON',
                                            'data': {
                                                'user_id': user_id,
                                                'user_name': new_user_name,
                                                'user_telephone_number': new_user_telephone_number,
                                                'user_comment': new_user_comment
                                            },
                                            success: function (result) {
                                                if (result.code == '888') {
                                                    window.location.href = '';
                                                }
                                            }
                                        });
                                    }
                                });


                            }
                        })

                    }
                })
            }
        })
    });


    function post_user_name(user_name) {
        $.ajax({
            'url': '/info/add_user_info/',
            'type': 'post',
            'data': {
                'user_name': user_name
            },
            success: function (result) {
                if (result.code == '888') {
                    var new_user_info = result.new_user_info;
                    var $add_user_info_tr = '<tr>' +
                        '<td><span></span></td>' +
                        '<td width="150px"><span>' + new_user_info['user_id'] + '</span></td>' +
                        '<td width="150px"><span>' + new_user_info['user_name'] + '</span></td>' +
                        '<td width="200px"><span>' + new_user_info['telephone_number'] + '</span></td>' +
                        '<td width="200px"><span>' + new_user_info['comment'] + '</span></td>' +
                        '<td width="300px"><span class="del_user_info" user_id="' + new_user_info['user_id'] + '">删除</span>&nbsp;&nbsp;|&nbsp;&nbsp; ' +
                        '<span user_id="' + new_user_info['user_id'] + '" class="change_user_info">修改</span></td>' +
                        '<td><span></span></td>' +
                        '</tr>';
                    $('#user_info_table_body tbody').append($add_user_info_tr);
                }
                else if (result.code == '000') {
                    Ewin.alert({message: '用户名 <b style="color: red;">' + user_name + '</b> 已存在...'}).on(function () {
                        $('#user_name').val('');
                        $('#user_name')[0].focus();
                    });
                }
            }
        })
    }
});