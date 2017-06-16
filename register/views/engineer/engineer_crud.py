from constance import config
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from common.views import get_form_edit_config, get_form_edit_url
from register.forms import EngineerForm, AddressForm, PhoneFormSetHelper, PhoneForm, UserForm
from common.views import *
from collections import namedtuple
from register.models import Engineer, Address, Telephone, ApplicationStatus
from common.forms import *
from django.http import HttpResponse

@login_required
@user_passes_test(approver_user, 'ife_register_login')
def engineer_new(request):
    return manage_engineer(request, None)

@login_required
@user_passes_test(engineer_user, 'ife_register_login')
def engineer_applicant_edit(request, user_pk):
    engineer = Engineer.objects.get(user_id=user_pk)
    return manage_engineer(request, engineer.id, True)

@login_required
@user_passes_test(approver_user, 'ife_register_login')
def engineer_edit(request, pk):
        return manage_engineer(request, pk, False)

def show_log(request):
    return request is None or (anonymous_user(request.user) == False and engineer_user(request.user) == False)

def get_user_for_engineer_form(request, engineer_id):
    if approver_user(request.user):
        try:
            engineer = Engineer.objects.get(pk=engineer_id)
            target_user = engineer.user
        except:
            target_user = None
    else:
        target_user = request.user
    return target_user


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_engineer(request, engineer_id=None, user_is_engineer = False):
    js_dict = {}
    del_request = None
    config = get_form_edit_config(engineer_id, None, Engineer, request, 'engineer_search')
    phone_helper = PhoneFormSetHelper()
    phone_form_set = get_phones_formset(config, engineer_id)
    target_user = get_user_for_engineer_form(request, engineer_id)

    if engineer_id is None:
        address = Address()
    else:
        address = config.primary_entity.address

    if engineer_id is not None:
        del_msg = 'You have successfully deleted the ' + config.class_name + ' ' + str(config.primary_entity)
        del_request = handle_delete_request(request, config, '/engineer_search', del_msg)
    if del_request is not None:
        return del_request
    elif request.method == "POST":
        # see also engineer_signup
        user_form = UserForm(request.POST, instance=target_user)
        primary_entity_form = EngineerForm(request.POST, request.FILES, instance=config.primary_entity, prefix=config.class_name,
                                           is_edit_form=config.is_edit_form, cancel_url=config.cancel_url, save_text=config.save_text)
        address_form = AddressForm(request.POST, request.FILES, instance=address, prefix="address")
        if user_form.is_valid() and primary_entity_form.is_valid() and address_form.is_valid() and phone_form_set.is_valid():
            address = address_form.save()
            created_primary_entity = primary_entity_form.save(commit=False)
            apply_auditable_info(created_primary_entity, request)
            created_primary_entity.address = address
            user_form.save()
            created_primary_entity.save()
            phone_form_set = get_phones_formset(config, engineer_id)
            save_many_relationship(phone_form_set)
            if request.POST.get("approve-app"):
                handle_engineer_approval(request, config.primary_entity)
            elif request.POST.get("reject-app"):
                handle_engineer_rejection(request, config.primary_entity)
            elif user_is_engineer and config.primary_entity.awaiting_approval():
                handle_engineer_modifed_application(request, config.primary_entity)
            elif user_is_engineer:
                handle_engineer_submitted(request, config.primary_entity)
            else:
                msg_once_only(request, 'Saved ' + config.class_name, settings.SUCC_MSG_TYPE)

            if user_is_engineer:
                action = '/engineer_app_edit/' + str(target_user.id)
            else:
                action = get_form_edit_url(None, created_primary_entity.id, config.class_name)
            return redirect(action)
    else:
        address_form = AddressForm(instance=address, prefix="address")
        user_form = UserForm(instance=target_user)
        primary_entity_form = EngineerForm(instance=config.primary_entity, prefix=config.class_name, is_edit_form=config.is_edit_form,
                                           cancel_url=config.cancel_url, save_text=config.save_text)

    if anonymous_user(request.user) == False and engineer_id is None:
        add_msg = 'Adding a new ' + config.class_name
        msg_once_only(request, add_msg, settings.WARN_MSG_TYPE)

    status_list = config.primary_entity.get_ordered_status()

    primary_entity_form_errors = form_errors_as_array(primary_entity_form)
    address_form_errors = form_errors_as_array(address_form)
    form_errors = primary_entity_form_errors + address_form_errors
    set_deletion_status_in_js_data(js_dict, request.user, admin_user)
    js_dict['show_log'] = show_log(request)
    set_deletion_status_in_js_data(js_dict, request.user, approver_user)
    js_data = json.dumps(js_dict)
    state_buttons = get_state_buttons_to_display(config, request)

    return render(request, 'engineer/engineer_edit.html', {'form': primary_entity_form,
                                                           'user_form': user_form,
                                                           'address_form': address_form,
                                                           'status_list' : status_list,
                                                           'phone_form_set': phone_form_set, 'phone_helper': phone_helper,
                                                           'js_data' : js_data,
                                                           'config' : config,
                                                           'state_buttons' : state_buttons,
                                                           'display_reject' : settings.DISPLAY_REJECT,
                                                           'display_approve' : settings.DISPLAY_APPROVE,
                                                           'form_errors': form_errors,})

def handle_engineer_submitted(request, engineer):
    # contact approver
    body = 'Engineer ' + engineer.get_full_name() + ' has submitted their details'
    from_add = config.GEN_FROM_EMAIL_ADDRESS
    to_add = config.APPROVER_EMAIL_ADDRESS
    cc = None
    bcc = None
    details = EmailDetails(body, body, 'Fire application submitted', from_add, to_add, cc, bcc)
    send_email(details, request, False)

    return handle_engineer_state_change(request, engineer, ApplicationStatus.SUB, 'submitted', False)

def handle_engineer_approval(request, engineer):
    return handle_engineer_state_change(request, engineer, ApplicationStatus.APP, 'approved')

def handle_engineer_rejection(request, engineer):
    return handle_engineer_state_change(request, engineer, ApplicationStatus.REJ, 'rejected')

def handle_engineer_modifed_application(request, engineer):
    body = 'Engineer ' + engineer.get_full_name() + ' has modified their details'
    from_add = config.GEN_FROM_EMAIL_ADDRESS
    to_add = config.APPROVER_EMAIL_ADDRESS
    cc = None
    bcc = None
    details = EmailDetails(body, body, 'Fire application modification', from_add, to_add, cc, bcc)
    send_email(details, request, False)


def handle_engineer_state_change(request, engineer, new_state, new_state_str, show_msg_sent = True):
    new_state = add_new_application_state(request, engineer, new_state)
    body = 'Dear ' + engineer.get_full_name()
    body += '<br>you application has been ' + new_state_str
    from_add = config.GEN_FROM_EMAIL_ADDRESS
    to_add = str(engineer.user.email)
    cc = None
    bcc = None
    details = EmailDetails(body, body, 'Fire application ' + new_state_str, from_add, to_add, cc, bcc)
    send_email(details, request, show_msg_sent)
    msg_once_only(request, new_state_str.capitalize(), settings.SUCC_MSG_TYPE)

    return new_state

def get_state_buttons_to_display(config, request):
    buttons = []
    latest_state = config.primary_entity.get_latest_status()
    if latest_state is not None:
        status = latest_state.status
        if engineer_can_be_approved(status, request):
            buttons.append(settings.DISPLAY_APPROVE)
        if engineer_can_be_rejected(status, request):
            buttons.append(settings.DISPLAY_REJECT)
    return buttons


def engineer_can_be_approved(status, request):
    return approver_user(request.user) and status == ApplicationStatus.SUB;


def engineer_can_be_rejected(status, request):
    return approver_user(request.user) and status == ApplicationStatus.SUB;


def get_phones_formset(config, engineer_id):
    return get_formset(config, Engineer, Telephone, PhoneForm, "phones", Telephone.objects.filter(engineer_id=engineer_id))


def add_new_application_state(request, engineer, status):
    app_state = ApplicationStatus(engineer=engineer, status=status)
    apply_auditable_info(app_state, request)
    app_state.save()

    return app_state
