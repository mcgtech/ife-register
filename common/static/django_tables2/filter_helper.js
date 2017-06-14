$(function(){
    setup_table_filters();
});

function setup_table_filters()
{
     remove_please_select();
     setup_filter_datepickers();
}

function remove_please_select()
{
     $("form select option:contains('Please select')").remove();
}

function setup_filter_datepickers()
{
    var options = get_basic_date_picker_options();
    $(".datepicker").datepicker(options);
}

function get_selected_entities()
{
    var id_selector = function() { return $(this).val(); };

    return $('tr td.selection input:checked').map(id_selector).get();
}