from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field


class EngineerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
                        Div(
                            Div('username', 'first_name', 'last_name', css_class="col-sm-6"),),
                            Div('email', 'password1', 'password2',  css_class="col-sm-6"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )