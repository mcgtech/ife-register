import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from common.views import get_form_edit_config, get_form_edit_url
from register.forms import EngineerForm, AddressForm, PhoneFormSetHelper, PhoneForm
from common.views import *
from collections import namedtuple
from register.models import Engineer, Address, Telephone
from common.forms import *

@login_required
@user_passes_test(admin_user, 'ife_register_login')
def engineer_new(request):
    return manage_engineer(request, None)


@login_required
@user_passes_test(admin_user, 'ife_register_login')
def engineer_edit(request, pk):
    return manage_engineer(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_engineer(request, engineer_id=None):
    js_dict = {}
    config = get_form_edit_config(engineer_id, None, Engineer, request, 'engineer_search')
    phone_helper = PhoneFormSetHelper()
    phone_form_set = get_phones_formset(config, engineer_id)
    msg = 'You have successfully deleted the ' + config.class_name + ' ' + str(config.primary_entity)

    if engineer_id is None:
        address = Address()
    else:
        address = config.primary_entity.address

    del_request = handle_delete_request(request, config, '/engineer_search', msg)
    if del_request:
        return del_request
    elif request.method == "POST":
        primary_entity_form = EngineerForm(request.POST, request.FILES, instance=config.primary_entity, prefix=config.class_name, is_edit_form=config.is_edit_form, cancel_url=config.cancel_url)
        address_form = AddressForm(request.POST, request.FILES, instance=address, prefix="address")
        if primary_entity_form.is_valid() and address_form.is_valid() and phone_form_set.is_valid():
            address = address_form.save()
            created_primary_entity = primary_entity_form.save(commit=False)
            apply_auditable_info(created_primary_entity, request)
            created_primary_entity.address = address
            created_primary_entity.save()
            phone_form_set = get_phones_formset(config, engineer_id)
            save_many_relationship(phone_form_set)
            msg_once_only(request, 'Saved ' + config.class_name, settings.SUCC_MSG_TYPE)
            action = get_form_edit_url(None, created_primary_entity.id, config.class_name)
            return redirect(action)
    else:
        address_form = AddressForm(instance=address, prefix="address")
        primary_entity_form = EngineerForm(instance=config.primary_entity, prefix=config.class_name, is_edit_form=config.is_edit_form, cancel_url=config.cancel_url)

    if engineer_id is None:
        add_msg = 'Adding a new ' + config.class_name
        msg_once_only(request, add_msg, settings.WARN_MSG_TYPE)

    primary_entity_form_errors = form_errors_as_array(primary_entity_form)
    address_form_errors = form_errors_as_array(address_form)
    form_errors = primary_entity_form_errors + address_form_errors
    set_deletion_status_in_js_data(js_dict, request.user, admin_user)
    js_data = json.dumps(js_dict)

    return render(request, 'engineer/engineer_edit.html', {'form': primary_entity_form,
                                                               'address_form': address_form,
                                                               'phone_form_set': phone_form_set, 'phone_helper': phone_helper,
                                                                  'js_data' : js_data,
                                                                  'config' : config,
                                                                  'form_errors': form_errors,})

def get_phones_formset(config, engineer_id):
    return get_formset(config, Engineer, Telephone, PhoneForm, "phones", Telephone.objects.filter(engineer_id=engineer_id))