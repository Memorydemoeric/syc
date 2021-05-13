$(function () {
    $('#close_window').click(function () {
        window.close();
    });

    $('#edit_statement_detail').on('click', function () {
        var pur_id = $(this).attr('pur_id');
        window.location.href = '/report/edit_report_detail/?pur_id=' + pur_id;
    });

    $('#storage_report_info_section').on('click', '#modify_translation_expense', function () {
        var pur_id = $('#storage_report_info_section').attr('pur_id');
        var old_translation_expense = parseFloat($('#translation_expense').text());
        $('#translation_expense').replaceWith('<input class="form-control" type="number" id="translation_expense_count" value="' + old_translation_expense + '" style="width: 10rem">');
        $(this).remove();
        $('#translation_expense_count')[0].focus();
        $('#translation_expense_count').on('keypress', function (ev) {
            if (ev.charCode == 13) {
                var new_translation_expense = $(this).val();
                if (!new_translation_expense) {
                    new_translation_expense = 0;
                }
                Ewin.confirm({message: '运费修改：&nbsp;&nbsp;' + old_translation_expense + '&nbsp;&nbsp;&nbsp;&nbsp;->&nbsp;&nbsp;&nbsp;&nbsp;' + new_translation_expense}).on(function (e) {
                    if (e) {
                        $.ajax({
                            'url': '/report/report_translation_expense_edit/',
                            'type': 'post',
                            'data': {
                                'old_translation_expense': old_translation_expense,
                                'new_translation_expense': new_translation_expense,
                                'pur_id': pur_id,
                            },
                            success: function (result) {
                                if (result.code == '888') {
                                    window.location.href = ''
                                }
                            }
                        })
                    }

                    else {
                        $('#translation_expense_count').replaceWith('<span id="translation_expense">' + old_translation_expense.toFixed(2) + '</span>');
                        $('#translation_expense_td').append('<span class="form-group" id="modify_translation_expense">修改</span></td>');
                    }


                });
            }
        })
    });

    $('#storage_report_info_section').on('click', '#change_trans_comment', function () {
        $('#trans_comment').replaceWith('<input type="text" class="form-control" id="trans_comment_text" style="width: 30rem">');
        $(this).remove();
        $('#trans_comment_text')[0].focus();
        $('#trans_comment_text').on('keypress', function (ev) {
            if (ev.charCode == 13) {
                var comment_containt = $(this).val();
                var pur_id = $('#storage_report_info_section').attr('pur_id');
                $.ajax({
                    'url': '/report/report_translation_comment_edit/',
                    'type': 'post',
                    'data': {
                        'comment_containt': comment_containt,
                        'pur_id': pur_id
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            window.location.href = ''
                        }
                    }
                });
            }
        })
    });


    $('#storage_report_info').on('click', '#change_handler', function () {
        var old_handler = $('#storage_handler').text();
        console.log(old_handler);
        $.ajax({
            'url': '/info/get_user_info/',
            'type': 'post',
            'async': false,
            'data': {
                'get_user_info': 'ok'
            },
            success: function (result) {
                if (result.code == '888') {
                    var $user_option = '';
                    for (i in result['user_info']) {
                        if (result['user_info'][i] == old_handler) {
                            $user_option += '<option selected="selected" value="' + i + '">' + result['user_info'][i] + '</option>'
                        }
                        else {
                            $user_option += '<option value="' + i + '">' + result['user_info'][i] + '</option>'
                        }
                    }
                    var $new_handler_select = '<select id="select_handler" class="form-control" style="width: 10rem">' + $user_option + '</select>';
                    $('#handler_contain').replaceWith('<span id="#handler">' + $new_handler_select + '</span>');

                }


                $('#storage_report_info').on('change', '#select_handler', function () {
                    var user_id = $(this).prop('selected', true).val();
                    var pur_id = $('#storage_report_info_section').attr('pur_id');
                    $.ajax({
                        'url': '/report/change_handler/',
                        'async': false,
                        'type': 'post',
                        'data': {
                            'user_id': user_id,
                            'pur_id': pur_id
                        },
                        success: function (result) {
                            if (result.code == '888') {
                                window.location.href = ''
                            }
                        }
                    })
                });


            }
        });

    });

});