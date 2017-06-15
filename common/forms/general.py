from django import forms
from django.core.validators import validate_email
from django.conf import settings
from django.shortcuts import redirect
from common.views import msg_once_only

def validate_required_field(self, field_name, field_name_desc):
    fld = self.cleaned_data[field_name]
    if not fld and fld != 0:
        error_msg = 'please enter a value for ' + field_name_desc
        self.form_errors.append(error_msg)
        raise forms.ValidationError(error_msg)
    return fld

def is_email_valid(email):
    try:
        validate_email( email )
        return True
    except forms.ValidationError:
        return False


def handle_delete_request(request, config, url, msg_suffix = ''):
    redir = None
    if config.primary_entity is not None and request.POST.get("delete-record"):
        msg = 'You have successfully deleted the ' + config.class_name + msg_suffix
        msg_once_only(request, msg, settings.INFO_MSG_TYPE)
        config.primary_entity.delete()
        redir = redirect(url)

    return redir

def get_base_ccy_prefix():
    return '£'