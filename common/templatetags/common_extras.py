from django import template
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

#https://stackoverflow.com/questions/4731572/django-counter-in-loop-to-index-list
@register.filter
def index(sequence, position):
    return sequence[position] if len(sequence) - 1 >= position else []

# http://stackoverflow.com/questions/34571880/how-to-check-in-template-whether-user-belongs-to-group
@register.filter(name='has_group')
def has_group(user, group_name):
    if user is not None:
        group = Group.objects.get(name=group_name)
        admin_group = Group.objects.get(name='admin')
        all_groups = user.groups.all()
        user_in_group = True if group in all_groups or admin_group in all_groups else False
        return user.is_superuser or user_in_group
    else:
        return None

@register.filter(name='has_strict_group')
def has_strict_group(user, group_name):
    if user is not None:
        group = Group.objects.get(name=group_name)
        all_groups = user.groups.all()
        user_in_group = True if group in all_groups else False
        return user_in_group
    else:
        return None

@register.filter(name='render_checkbox')
def render_checkbox(checked):
    # icon = 'glyphicon-ok' if checked else 'glyphicon-remove'
    # return mark_safe('<span class="glyphicon ' + icon + '"></span>')
    # checked = 'checked' if checked else ''
    # return mark_safe('<input type="checkbox" ' + checked + '>')
    # https://stackoverflow.com/questions/658044/tick-symbol-in-html-xhtml
    markup = '&#x2714;' if checked else '&#x2718;'
    return mark_safe(markup)

@register.filter(name='format_model_choice')
def format_model_choice(choice):
    return 'Not selected' if choice == 'Please select' else choice