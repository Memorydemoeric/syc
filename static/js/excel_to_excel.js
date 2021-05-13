$(function () {
    $('#change_purchase').click(function () {
        $('#file_upload').click();
    });

    $('#file_upload').change(function () {
        var $form_data = new FormData();
        var $file_info = $('#file_upload')[0].files[0];
        var $file_name = $('#file_upload').val();
        var $str_file_name = $file_name.replace(/^.+?\\([^\\]+?)(\.[^\.\\]*?)?$/gi,"$1");
        $form_data.append('file_upload', $file_info);
        $form_data.append('file_name', $str_file_name);
        $.ajax({
            'url': '/system/excel_to_excel/',
            'type': 'post',
            'data': $form_data,
            'processData': false,
            'contentType': false,
            success:
                function (result) {
                    if (result.code) {
                    $('#translation_download').attr('href', '/system/translate_file_down/?file_name=' + result.code)
                        document.getElementById('translation_download').click();
                    window.location.href = '/system/excel_to_excel/'
                    }
                }
        });
    });
});
