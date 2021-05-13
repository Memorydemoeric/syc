$(function () {
    $('#close_window').click(function () {
        window.close();
    });

    $('#modify_translation_expense').on('click', function () {
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
        })
    });

});