from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from register.forms import *
from django.conf import settings
from django.contrib.auth.models import Group

def engineer_signup(request):
    if request.method == 'POST':
        form = EngineerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            engineer = Engineer.objects.create(user=user) # see also engineer_group_receiver for when user added to engineer group via admin
            engineer.save()
            engineer_group = Group.objects.get(name=settings.ENGINEER_GROUP)
            engineer_group.user_set.add(user)
            engineer_group.save()
            return redirect('engineer_app_edit', user_pk=user.id)
    else:
        form = EngineerSignUpForm()
    return render(request, 'engineer/engineer_signup.html', {'form': form})