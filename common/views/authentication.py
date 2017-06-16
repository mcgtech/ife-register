from django.conf import settings
from register.models import Engineer

def admin_user(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists()

def approver_user(user):
    return admin_user(user) or user.groups.filter(name=settings.APPROVER_GROUP).exists()

def engineer_user(user, strict = False):
    in_target_group = user.groups.filter(name=settings.ENGINEER_GROUP).exists()
    if strict:
        return in_target_group
    else:
        return admin_user(user) or in_target_group

def allow_engineer_edit(user, pk_engineer):
    allow = False
    if admin_user(user):
        allow = True
    elif engineer_user(user, True):
        try:
            engineer_assoc_with_user = Engineer.objects.get(user_id=user.id)
            allow = int(engineer_assoc_with_user.id) == int(pk_engineer)
        except:
            allow = False
    return allow

def anonymous_user(user):
    return user.is_anonymous()

def show_form_error(request, messages, msg, inform_support):
    messages.error(request, msg)

def set_deletion_status_in_js_data(js_dict, user, security_fn):
    js_dict['delete_allowed'] = security_fn(user)
