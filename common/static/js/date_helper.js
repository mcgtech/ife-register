function get_basic_date_picker_options()
{
    return {
              changeMonth: true,
              changeYear: true,
              dateFormat: 'dd/mm/yy'
           };
}

function apply_datepicker_on_add_event(block_id, options)
{
    // add datepicker to new quals row date
    var options = get_basic_date_picker_options();
    // I do it like this as otherwise it desnt work correctly
    var picker_elems = $('#' + block_id + ' .datepicker');
    picker_elems.datepicker('destroy');
    picker_elems.datepicker(options);
}