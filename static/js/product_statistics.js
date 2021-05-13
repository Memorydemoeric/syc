$(function () {
    var body_section_width = $('#report_statistics_title').parent('section').width();
    $('#report_statistics_body_section').css('width', parseFloat(body_section_width) + 45.00 + 'px');

    $(window).resize(function () {
        var body_section_width = $('#report_statistics_title').parent('section').width();
        $('#report_statistics_body_section').css('width', parseFloat(body_section_width) + 45.00 + 'px');
    });

    $('#start_date')[0].select();

    $('#order_by_button').on('click', function (e) {
        e.preventDefault();
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        var order_by = $(this).attr('data-order_by');
        window.location.href = '?start_date=' + start_date + '&end_date=' + end_date + '&order_by=' + order_by;
    });

    $('#start_date').on('keypress', function (e) {
        if (e.charCode == 13) {
            $('#end_date').select();
        }
    });

    $('#end_date').on('keypress', function (e) {
        if (e.charCode == 13) {
            search_statistics_by_date();
        }
    });


    $('#submit_search_statistics').on('click', function () {
        search_statistics_by_date();
    });


    function search_statistics_by_date() {
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        window.location.href = '?start_date=' + start_date + '&end_date=' + end_date;
    }


});
