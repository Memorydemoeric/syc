$(function () {


//    /report/report_type_date/


    $('#cust_condition').on('keypress', function (e) {
        e.preventDefault();
        if (e.charCode == 13) {
            $('#date_start')[0].focus();
        }
    });

    $('#date_start').on('keypress', function (e) {
        e.preventDefault();
        if (e.charCode == 13) {
            $('#date_end')[0].focus();
        }
    });


});