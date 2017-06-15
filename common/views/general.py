from django.conf import settings
from django.shortcuts import render
from django.contrib.messages import get_messages
from django.contrib.messages import info, success, warning, error, debug
from collections import namedtuple
from django.shortcuts import get_object_or_404, redirect
from django.forms import inlineformset_factory
from common.views.auditable import apply_auditable_info
from common.views.authentication import *

def home_page(request):
    return render(request, 'home_page.html', {})

# the following methods are used for views for entities that belong to a parent - eg interview
EditConfig = namedtuple('EditConfig', 'primary_entity the_action_text is_edit_form action can_delete class_name cancel_url primary_id request parent_id save_text')
# primary_id is the id of the entity being editied
def get_form_edit_config(primary_id, parent_id, primary_class, request, cancel_redirect_name):
    if primary_id is None:
        primary_entity = primary_class()
        the_action_text = 'Create'
        is_edit_form = False
        can_delete = False
    else:
        primary_entity = get_object_or_404(primary_class, pk=primary_id)
        can_delete = True
        the_action_text = 'Edit'
        is_edit_form = True

    class_name = primary_entity.__class__.__name__.lower()
    if primary_id is None:
        action = get_form_add_url(parent_id, class_name)
    else:
        action = get_form_edit_url(parent_id, primary_id, class_name)

    if request.method == "POST":
        cancel_url = None
    else:
        if parent_id is not None:
            cancel_url = redirect(cancel_redirect_name, pk=parent_id).url
        else:
            cancel_url = redirect(cancel_redirect_name).url
    save_text = ''
    if applicant_user(request.user):
        save_text = 'Submit Application'
    if engineer_user(request.user):
        save_text = 'Submit Changes'

    return EditConfig(primary_entity, the_action_text, is_edit_form, action, can_delete, class_name, cancel_url, primary_id, request, parent_id, save_text)


def get_form_add_url(parent_id, class_name):
    url = '/' + class_name
    if parent_id is not None:
        url = url+ '/' + str(parent_id)
    url = url +  '/new/'

    return url

def get_form_edit_url(parent_id, primary_id, class_name):
    url = '/' + class_name
    if parent_id is not None:
        url = url + '/' + str(parent_id)
    url = url + '/' + str(primary_id) + '/edit/'

    return url

# http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def form_errors_as_array(form):
    errors = []
    if (form.errors and len(form.errors) > 0):
        for error in form.errors.items():
            errors.append(remove_html_tags(str(error[1])))

    return errors

# https://jorlugaqui.net/2016/02/20/how-to-strip-html-tags-from-a-string-in-python/
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# https://stackoverflow.com/questions/23249807/django-remove-duplicate-messages-from-storage/25157660#25157660
def msg_once_only(request, msg, type):
    """
    Just add the message once
    :param request:
    :param msg:
    :return:
    """
    storage = get_messages(request)
    if msg not in [m.message for m in storage]:
        if (type == settings.INFO_MSG_TYPE):
            info(request, msg)
        elif (type == settings.SUCC_MSG_TYPE):
            success(request, msg)
        elif (type == settings.WARN_MSG_TYPE):
            warning(request, msg)
        elif (type == settings.ERR_MSG_TYPE):
            error(request, msg)
        elif (type == settings.DEBUG_MSG_TYPE):
            debug(request, msg)
    storage.used = False # to ensure we dont clear the messages we got in storage = get_messages(request)

def get_force_page_break_markup():
    return '<div style="display: block; page-break-after: always; position: relative;"></div>'

def get_formset(config, parent_model, model, form, prefix, set):
    # setup formsets
    if config.primary_id is None:
        FormSet = inlineformset_factory(parent_model, model, form=form, extra=1, can_delete=config.can_delete)
    else:
        FormSet = inlineformset_factory(parent_model, model, form=form, extra=get_extras_for_formset(set), can_delete=config.can_delete)

    if config.request.method == "POST":
        form_set = FormSet(config.request.POST, config.request.FILES, instance=config.primary_entity, prefix=prefix)
    else:
        form_set = FormSet(instance=config.primary_entity, prefix=prefix)

    return form_set


def get_extras_for_formset(set):
    return 1 if len(set) == 0 else 0



def save_many_relationship(form_set, auditable = False, request = None, target = None):
    for form in form_set.forms:
        if form.has_changed():
            if form in form_set.deleted_forms:
                form.instance.delete()
            else:
                # for some reason modified_by and modified_date always come back as changed so need to do the
                # changed_data check
                if auditable and target in form.changed_data:
                    instance = form.save(commit = False)
                    apply_auditable_info(instance, request)
                    instance.save()
                else:
                    form.save()