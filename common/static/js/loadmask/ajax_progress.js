$(function(){
    setup_ajax_in_progress_for_page();
})

function setup_ajax_in_progress_for_page()
{
    var section = $('body');
    $(document).bind("ajaxSend", function () {
        show_process_mask(section, true);
    }).bind("ajaxComplete", function () {
        show_process_mask(section, false);
    });
}


function show_process_mask(section, show)
{
    if (show)
    {
        section.mask("Processing request, please wait...");
    }
    else
    {
        section.unmask();
    }
}