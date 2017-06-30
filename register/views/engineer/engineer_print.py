
from register.models import Engineer
from django.shortcuts import render
def print_engineer(request, eng_id):
    engineer = Engineer.objects.get(pk=eng_id)
    return render(request, 'engineer/engineer_print.html', {'engineer': engineer})