$(function () {

    $('input').on('click', function (ev) {
        ev.stopPropagation();
    });


    $('tbody.action_warning').on('mouseenter', 'tr', function () {
        var str = $(this).attr('class') || 'nothing';
        var reg = RegExp('control_tr');
        if (!str.match(reg)) {
            $(this).css('background-color', '#c8c8c8');
            $(this).addClass('selected_tr')
        }
    });

    $('tbody.action_warning').on('mouseleave', '.selected_tr', function () {
        var str = $(this).attr('class');
        var reg = RegExp('control_tr');
        if (!str.match(reg)) {
            $(this).removeClass('selected_tr');
            $(this).css('background-color', '')
        }

    });


    $('tbody.action_warning').on('click', 'tr', function () {
        var str = $(this).attr('class');
        var reg = RegExp('control_tr');
        if (!str.match(reg)) {
            $('.control_tr').css('background-color', '');
            $('.control_tr').removeClass('control_tr');
            $(this).css('background-color', '#fdffa7');
            $(this).addClass('control_tr')
        }
        else {
            $(this).removeClass('control_tr');
            $(this).css('background-color', '');
        }

    });


    $(document).on('keydown', function (ev) {
        if (ev.keyCode == 87 && !$('input:text:focus').length) {
            var $control_tr = $('.control_tr');
            var section_height = $('.control_tr').parents('section').height();
            var section_scroll_top = $('.control_tr').parents('section').scrollTop();
            if ($control_tr.prev().length) {
                $control_tr.css('background-color', '');
                $control_tr.prev().css('background-color', '#fdffa7');
                $control_tr.removeClass('control_tr');
                $control_tr.prev().addClass('control_tr');
                auto_scroll($control_tr, ev.keyCode);
            }

        }
        if (ev.keyCode == 83 && !$('input:text:focus').length) {
            var $control_tr = $('.control_tr');
            if ($control_tr.next().length) {
                $control_tr.css('background-color', '');
                $control_tr.next().css('background-color', '#fdffa7');
                $control_tr.removeClass('control_tr');
                $control_tr.next().addClass('control_tr');
                auto_scroll($control_tr, ev.keyCode);
            }
        }
    });


    function auto_scroll(control_tr, key_code) {
        var section_height = control_tr.parents('section').height();
        var section_scroll_top = control_tr.parents('section').scrollTop();
        var tr_offset = control_tr.position().top;
        if (tr_offset <= 50 && key_code == 87) {
            section_scroll_top -= (section_height - 50);
            control_tr.parents('section').scrollTop(section_scroll_top);
        }
        else if (tr_offset >= section_height - 50 && key_code == 83) {
            section_scroll_top += (section_height - 50);
            control_tr.parents('section').scrollTop(section_scroll_top);
        }

    }


});