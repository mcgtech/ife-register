from django.conf import settings

def admin_user(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists()

def approver_user(user):
    return admin_user(user) or user.groups.filter(name=settings.APPROVER_GROUP).exists()

def engineer_user(user):
    return admin_user(user) or user.groups.filter(name=settings.ENGINEER_GROUP).exists()

def anonymous_user(user):
    return user.is_anonymous()

def show_form_error(request, messages, msg, inform_support):
    messages.error(request, msg)

def set_deletion_status_in_js_data(js_dict, user, security_fn):
    js_dict['delete_allowed'] = security_fn(user)
