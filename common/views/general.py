from django.conf import settings
from django.shortcuts import render
from django.contrib.messages import get_messages
from django.contrib.messages import info, success, warning, error, debug
from collections import namedtuple
from django.shortcuts import get_object_or_404, redirect
from django.forms import inlineformset_factory
from common.views.auditable import apply_auditable_info
from common.views.authentication import *
from django.core.mail import EmailMultiAlternatives
from register.models import ApplicationStatus

def login_success(request):
    if engineer_user(request.user, True):
        # user is an admin
        return redirect("engineer_app_edit", user_pk=request.user.pk)
    else:
        return redirect("engineer_search")

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
    if engineer_user(request.user) and primary_entity.awaiting_approval():
        save_text = 'Submit Your Application'
    elif engineer_user(request.user) and (primary_entity.rejected() or primary_entity.expired()):
        save_text = 'Resubmit Your Application'
    elif engineer_user(request.user):
        save_text = 'Submit Your Changes'
    else:
        save_text = 'Save'

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


def get_query_by_key(request, key):
    value = None
    if request.GET is not None and key in request.GET:
        value = request.GET[key]
    return value

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

EmailDetails = namedtuple('EmailDetails', 'html_body plain_body subject from_address to_addresses cc_addresses bcc_addresses')
def send_email(details, request, show_msg_sent = True):
    html_content = details.html_body
    plain_content = details.plain_body
    subject = details.subject
    from_email = details.from_address
    to_addresses = details.to_addresses.split(",")
    cc_addresses = details.cc_addresses.split(",") if details.cc_addresses is not None else ''
    bcc_addresses = details.bcc_addresses.split(",") if details.bcc_addresses is not None else ''
    # https://docs.djangoproject.com/en/1.11/topics/email/
    try:
        email = EmailMultiAlternatives(
            subject = subject,
            body = plain_content,
            from_email = from_email,
            to = to_addresses,
            cc = cc_addresses,
            bcc = bcc_addresses,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(False)
        if show_msg_sent:
            msg_once_only(request, 'Email sent to ' + str(to_addresses), settings.SUCC_MSG_TYPE)
    except Exception as e:
        msg_once_only(request, 'Failed to email ' + str(to_addresses) + ' as an exception occurred: ' + str(e), settings.ERR_MSG_TYPE)


def add_test_user(first, last, emp, l1, l2, l3, pc, town, tit, max_state, ife_grade):
    from django.contrib.auth.models import User
    from register.models import Engineer, Address, ApplicationStatus, Telephone
    from datetime import datetime
    eng = Engineer()
    username = first.lower() + '_' + last.lower()
    try:
        eng_user = User.objects.get(username=username)
    except:
        eng_user = User.objects.create_user(username, 'annlee@shirlie.co.uk', username + '123')
    eng_user.first_name=first
    eng_user.last_name=last
    eng_user.email=username + '@gmail.com'
    eng_user.save()
    eng.user=eng_user

    eng.title = tit
    eng.employer = emp
    address = Address()
    address.line_1 = l1
    address.line_2 = l2
    address.line_3 = l3
    address.post_town = town
    address.post_code = pc
    address.save()
    eng.address = address
    eng.pi_insurance_cover = 10000
    eng.pi_renewal_date = '2018-6-2'
    eng.pi_company = 'Robust Ins inc'
    eng.build_std_know = 'I helped draft it.'
    eng.type_of_work = 'I have been a regulator for 3 years.'
    eng.ife_member_grade = ife_grade
    eng.ife_member_no = 'AF458-997'
    eng.ife_member_reg_date = '2009-4-3'
    eng.ec_member_grade = 5
    eng.ec_member_no = '435095890'
    eng.ec_member_reg_date = '2011-9-21'
    eng.cpd = 'I attend two training courses every year.'
    eng.created_by = eng_user
    eng.modified_by = eng_user
    eng.created_on = datetime.now()
    eng.modified_on = datetime.now()
    eng.save()

    tele=Telephone(type=0, number='01463 716099', engineer=eng)
    tele.save()


    state = ApplicationStatus(status=0, engineer=eng)
    state.created_by = eng_user
    state.modified_by = eng_user
    state.created_on = datetime.now()
    state.modified_on = datetime.now()
    state.save()

    if max_state > 0:
        state = ApplicationStatus(status=1, engineer=eng)
        state.created_by = eng_user
        state.modified_by = eng_user
        state.created_on = datetime.now()
        state.modified_on = datetime.now()
        state.save()

    if max_state > 1:
        state = ApplicationStatus(status=2, engineer=eng)
        app_user = User.objects.get(username='approver')
        state.created_by = app_user
        state.modified_by = app_user
        state.created_on = datetime.now()
        state.modified_on = datetime.now()
        state.save()

    if max_state > 2:
        state = ApplicationStatus(status=3, engineer=eng)
        app_user = User.objects.get(username='approver')
        state.created_by = app_user
        state.modified_by = app_user
        state.created_on = datetime.now()
        state.modified_on = datetime.now()
        state.save()
