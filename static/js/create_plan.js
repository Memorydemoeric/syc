$(function () {

    $('#pro_id').focus();

    $('.del_plan_detail').click(function () {
        var $select_detail = $(this);
        $.ajax({
            'url': '/plan/del_plan_detail/',
            'type': 'post',
            'data': {
                'pro_id': $select_detail.attr('name')
            },
            success: function (result) {
                if (result.code == '888') {
                }
            }
        })
    });

    $('#pro_id').keypress(function (ev) {
        if (ev.charCode == 13) {
            $('#pro_count').focus();
            $('#pro_count').keypress(function (ev) {
                if (ev.charCode == 13) {
                    var $pro_id = $('#pro_id').val();
                    var $pro_count = $(this).val();
                    if ($pro_id && $pro_count) {
                        $.ajax({
                            'url': '/plan/add_plan_detail/',
                            'type': 'post',
                            'data': {
                                'pro_id': $pro_id,
                                'pro_count': $pro_count,
                            },
                            success: function (result) {
                                if (result.code == '888') {
                                    window.location.href = '/plan/create_plan/'
                                }
                            }
                        })
                    }

                }
            })
        }
    });


    $('#plan_detail_submit').click(function () {
        var $pro_id = $('#pro_id').val();
        var $pro_count = $(this).val();
        if ($pro_id && $pro_count) {
            $.ajax({
                'url': '/plan/add_plan_detail/',
                'type': 'post',
                'data': {
                    'pro_id': $pro_id,
                    'pro_count': $pro_count,
                },
                success: function (result) {
                    if (result.code == '888') {
                        window.location.href = '/plan/create_plan/'
                    }
                }
            })
        }
    });


    $('#clear_plan').click(function () {
        window.location.href = '/plan/clear_plan_detail/'
    });

    $('#submit_plan').click(function () {
        $.ajax({
            'url': '/plan/submit_plan_detail/',
            'type': 'post',
            'data': '888',
            success: function (result) {
                if (result.code) {
                    $('#plan_download').attr('href', '/plan/file_down/?file_name=' + result.code);
                    document.getElementById("plan_download").click();

                    //注册完成按钮的事件
                    Ewin.confirm({message: "文件创建成功？"}).on(function (e) {
                        if (!e) {
                            return;
                        }
                        else {
                            $.ajax({
                                'url': '/plan/clear_rds/',
                                'type': 'post',
                                'data': 'del_rds',
                                success: function (result) {
                                    if (result.code) {
                                        window.location.href = '/plan/';
                                    }
                                }
                            });
                        }
                    });


                }
            }
        });
    })

});