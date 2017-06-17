$(function(){
    setup_contact_details();
    setup_datepickers();
    handle_log_visibility();
    setup_app_status();
    add_printing();
});

function add_printing()
{
    $('#print-eng').click(function(){
        var url = '/print_engineer/' + data_from_django.eng_id + '/';
        $('#print_area').html('').load(url, '', function(response, status, xhr) {
            if (status == 'error')
            {
                var msg = "Sorry but there was a printing error: " + xhr.status + " " + xhr.statusText;
                bootbox.alert(msg);
            }
            else
            {
                $('#print_area').printThis();
            }
            });
    });
}

function setup_app_status()
{
    $('#app_status_table').appendTo('#application-status');
}

function handle_log_visibility()
{
    if (data_from_django.show_log)
    {
        $('#engineer_edit_form li:last-child').show();
    }
}

function setup_contact_details()
{
    $('#user').insertAfter('#div_id_engineer-title');
    $('#address').appendTo('.address');
    var phones_elem = $('#phones');
    phones_elem.appendTo('.name_con');
    setup_phone_formsets();
    $('<label class="control-label ">Telephone</label>').insertBefore($('table', phones_elem));
}

function setup_phone_formsets()
{
    setTimeout(function(){
            $('#phones tbody tr').formset({prefix: 'phones'});
        }, 10);
}

function setup_datepickers()
{
    var options = get_basic_date_picker_options();
    $("#id_engineer-pi_renewal_date").datepicker(options);
}