$(function () {
    $('#cust_location')[0].focus();
    $('#search_cust').click(function () {
        var $location = $('#cust_location').val();
        window.location.href = '/info/customer_info/?location=' + $location;
    });


    $('#input_customer').click(function () {
        $('#file_upload').click();
    });
    $('#file_upload').change(function () {
        Ewin.confirm({message: '确定导入客户信息?'}).on(function (ev) {
            if (!ev) {
                return
            }
            else {
                var $file_name = $('#file_upload').val();
                var $file_type = $file_name.substr($file_name.length - 4, $file_name.length);
                var $file_data = new FormData();
                $file_data.append('excel', $('#file_upload')[0].files[0]);
                $.ajax({
                    url: '/info/upload_customer_info/',
                    type: 'POST',
                    async: false,
                    data: $file_data,
                    contentType: false,
                    processData: false,
                    success: function (result) {
                        if (result.code == '888') {
                            Ewin.alert({message: '导入成功...'}).on(function (e) {
                                if (e) {
                                    window.location.href = '';
                                }
                            });
                        }
                        else if (result.code == '000') {
                            Ewin.alert({message: '请检查文件内容...'}).on(function (e) {
                                if (e) {
                                    window.location.href = '';
                                }
                            });
                        }
                    }
                })
            }
        })
    });


    $('#cust_location').keypress(function (ev) {
        var $location = $('#cust_location').val();
        if (ev.charCode == '13') {
            window.location.href = '/info/customer_info/?location=' + $location;
        }
    });

    $('.delete_customer_detail').click(function () {
        var $pro_id = $(this).prev().attr('cust_id');
        Ewin.confirm({message: '删除客户信息？'}).on(function (ev) {
            if (ev) {
                $.ajax({
                    url: '/info/delete_customer_info/',
                    type: 'post',
                    data: {
                        'pro_id': $pro_id,
                    },
                    success: function (result) {
                        if (result.code == '888') {
                            $('#row_' + $pro_id).remove();
                        }
                    }
                })
            }
        })
    });


    $('#create_customer').click(function () {
        var $cust_location;
        var $cust_name;
        var $cust_mobilephone;
        var $cust_phone;
        var $cust_address;
        var $cust_rebate;
        $('#customer_info tbody').append('                <tr class="new_row">' +
            '                    <td width="10%"><input type="text" id="input_cust_location" style="width: 8rem;"></td>' +
            '                    <td width="10%"><span id="cust_name"></span></td>' +
            '                    <td width="10%"><span id="cust_mobilephone"></span></td>' +
            '                    <td width="10%"><span id="cust_phone"></span></td>' +
            '                    <td width="35%"><span id="cust_address"></span></td>' +
            '                    <td width="5%"><span id="cust_rebate"></span></td>' +
            '                    <td width="20%">' +
            '                    <span type="finish" pro_id="" class="edit_customer_detail">修改</span>&nbsp;&nbsp;|&nbsp;&nbsp;' +
            '                    <span class="delete_customer_detail">删除</span>' +
            '                    </td></tr>');


        $('#input_cust_location')[0].focus();
        $('#customer_info').scrollTop = 100000;
        $('td').on('keypress', '#input_cust_location', function (ev) {
            if (ev.charCode == '13') {
                $cust_location = $('#input_cust_location').val();
                $(this).parent().replaceWith('<td width="10%">' + $cust_location + '</td>');
                $('#cust_name').replaceWith('<input type="text" id="cust_name" style="width: 8rem;">');
                $('#cust_name')[0].focus();
                $('td').on('keypress', '#cust_name', function (ev) {
                    if (ev.charCode == '13') {
                        $cust_name = $('#cust_name').val();
                        $(this).parent().replaceWith('<td width="10%">' + $cust_name + '</td>');
                        $('#cust_mobilephone').replaceWith('<input type="text" id="cust_mobilephone" style="width: 8rem;">');
                        $('#cust_mobilephone')[0].focus();
                        $('td').on('keypress', '#cust_mobilephone', function (ev) {
                            if (ev.charCode == '13') {
                                $cust_mobilephone = $('#cust_mobilephone').val();
                                $(this).parent().replaceWith('<td width="10%">' + $cust_mobilephone + '</td>');
                                $('#cust_phone').replaceWith('<input type="text" id="cust_phone" style="width: 8rem;">');
                                $('#cust_phone')[0].focus();
                                $('td').on('keypress', '#cust_phone', function (ev) {
                                    if (ev.charCode == '13') {
                                        $cust_phone = $('#cust_phone').val();
                                        $(this).parent().replaceWith('<td width="10%">' + $cust_phone + '</td>');
                                        $('#cust_address').replaceWith('<input type="text" id="cust_address" style="width: 25rem;">');
                                        $('#cust_address')[0].focus();
                                        $('td').on('keypress', '#cust_address', function (ev) {
                                            if (ev.charCode == '13') {
                                                $cust_address = $('#cust_address').val();
                                                $(this).parent().replaceWith('<td width="35%">' + $cust_address + '</td>');
                                                $('#cust_rebate').replaceWith('<input type="number" id="cust_rebate" style="width: 5rem;">');
                                                $('#cust_rebate')[0].focus();
                                                $('td').on('keypress', '#cust_rebate', function (ev) {
                                                    if (ev.charCode == '13') {
                                                        $cust_rebate = $('#cust_rebate').val();
                                                        $(this).parent().replaceWith('<td width="5%">' + parseFloat($cust_rebate).toFixed(2) + '</td>');
                                                        Ewin.confirm({message: '确认创建该客户信息？'}).on(function (ev) {
                                                            if (!ev) {
                                                                $('.new_row:last').remove();
                                                            }
                                                            else {
                                                                $.ajax({
                                                                    url: '/info/add_customer_info/',
                                                                    type: 'post',
                                                                    data: {
                                                                        'cust_location': $cust_location,
                                                                        'cust_name': $cust_name,
                                                                        'cust_mobilephone': $cust_mobilephone,
                                                                        'cust_phone': $cust_phone,
                                                                        'cust_address': $cust_address,
                                                                        'cust_rebate': $cust_rebate,
                                                                    },
                                                                    success: function (result) {
                                                                        if (result.code == '888') {
                                                                            window.location.href = ''
                                                                        }
                                                                    }
                                                                })
                                                            }
                                                        })

                                                    }
                                                })

                                            }
                                        })

                                    }
                                })

                            }
                        })
                    }
                })
            }
        })


    });


    $('.edit_customer_detail').click(function () {
        var $cust_location;
        var $cust_name;
        var $cust_mobilephone;
        var $cust_phone;
        var $cust_address;
        var $cust_rebate;
        var $cust_id = $(this).attr('cust_id');

        var $old_cust_location = $('#input_cust_location_' + $cust_id).text();
        var $old_cust_name = $('#cust_name_' + $cust_id).text();
        var $old_cust_mobilephone = $('#cust_mobilephone_' + $cust_id).text();
        var $old_cust_phone = $('#cust_phone_' + $cust_id).text();
        var $old_cust_address = $('#cust_address_' + $cust_id).text();
        var $old_cust_rebate = $('#cust_rebate_' + $cust_id).text();

        $('#input_cust_location_' + $cust_id).replaceWith('<input type="text" id="input_cust_location" style="width: 8rem;">');
        $('#input_cust_location')[0].focus();
        $('td').on('keypress', '#input_cust_location', function (ev) {
            if (ev.charCode == '13') {
                if ($('#input_cust_location').val()) {
                    $cust_location = $('#input_cust_location').val();
                }
                else {
                    $cust_location = $old_cust_location;
                }
                $(this).parent().replaceWith('<td width="10%">' + $cust_location + '</td>');
                $('#cust_name_' + $cust_id).replaceWith('<input type="text" id="cust_name" style="width: 8rem;">');
                $('#cust_name')[0].focus();
                $('td').on('keypress', '#cust_name', function (ev) {
                    if (ev.charCode == '13') {
                        if ($('#cust_name').val()) {
                            $cust_name = $('#cust_name').val();
                        }
                        else {
                            $cust_name = $old_cust_name;
                        }
                        $(this).parent().replaceWith('<td width="10%">' + $cust_name + '</td>');
                        $('#cust_mobilephone_' + $cust_id).replaceWith('<input type="text" id="cust_mobilephone" style="width: 8rem;">');
                        $('#cust_mobilephone')[0].focus();
                        $('td').on('keypress', '#cust_mobilephone', function (ev) {
                            if (ev.charCode == '13') {
                                if ($('#cust_mobilephone').val()) {
                                    $cust_mobilephone = $('#cust_mobilephone').val();
                                }
                                else {
                                    $cust_mobilephone = $old_cust_mobilephone;
                                }
                                $(this).parent().replaceWith('<td width="10%">' + $cust_mobilephone + '</td>');
                                $('#cust_phone_' + $cust_id).replaceWith('<input type="text" id="cust_phone" style="width: 8rem;">');
                                $('#cust_phone')[0].focus();
                                $('td').on('keypress', '#cust_phone', function (ev) {
                                    if (ev.charCode == '13') {
                                        if ($('#cust_phone').val()) {
                                            $cust_phone = $('#cust_phone').val();
                                        }
                                        else {
                                            $cust_phone = $old_cust_phone;
                                        }
                                        $(this).parent().replaceWith('<td width="10%">' + $cust_phone + '</td>');
                                        $('#cust_address_' + $cust_id).replaceWith('<input type="text" id="cust_address" style="width: 25rem;">');
                                        $('#cust_address')[0].focus();
                                        $('td').on('keypress', '#cust_address', function (ev) {
                                            if (ev.charCode == '13') {
                                                if ($('#cust_address').val()) {
                                                    $cust_address = $('#cust_address').val();
                                                }
                                                else {
                                                    $cust_address = $old_cust_address;
                                                }
                                                $(this).parent().replaceWith('<td width="35%">' + $cust_address + '</td>');
                                                $('#cust_rebate_' + $cust_id).replaceWith('<input type="number" id="cust_rebate" style="width: 5rem;">');
                                                $('#cust_rebate')[0].focus();
                                                $('td').on('keypress', '#cust_rebate', function (ev) {
                                                    if (ev.charCode == '13') {
                                                        if ($('#cust_rebate').val()) {
                                                            $cust_rebate = $('#cust_rebate').val();
                                                        }
                                                        else {
                                                            $cust_rebate = $old_cust_rebate;
                                                        }
                                                        $(this).parent().replaceWith('<td width="5%">' + parseFloat($cust_rebate).toFixed(2) + '</td>');
                                                        Ewin.confirm({message: '修改客户信息？'}).on(function (ev) {
                                                            if (!ev) {
                                                                window.location.href = '';
                                                            }
                                                            else {
                                                                $.ajax({
                                                                    url: '/info/edit_customer_info/',
                                                                    type: 'post',
                                                                    data: {
                                                                        'cust_id': $cust_id,
                                                                        'cust_location': $cust_location,
                                                                        'cust_name': $cust_name,
                                                                        'cust_mobilephone': $cust_mobilephone,
                                                                        'cust_phone': $cust_phone,
                                                                        'cust_address': $cust_address,
                                                                        'cust_rebate': $cust_rebate,
                                                                    },
                                                                    success: function (result) {
                                                                        if (result.code == '888') {
                                                                            window.location.href = '';
                                                                        }
                                                                    }
                                                                })
                                                            }
                                                        })

                                                    }
                                                })

                                            }
                                        })

                                    }
                                })

                            }
                        })
                    }
                })
            }
        })


    })


});