$(function(){
    setup_contact_details();
    setup_datepickers();
    handle_log_visibility();
});

function handle_log_visibility()
{
    if (data_from_django.show_log)
    {
        $('#engineer_edit_form li:last-child').show();
    }
}

function setup_contact_details()
{
    $('#address').appendTo('.address');
    var phones_elem = $('#phones');
    phones_elem.appendTo('.name_con');
    setup_phone_formsets();
    phones_elem.prepend('<label for="id_main-middle_name" class="control-label ">Telephone</label>');
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