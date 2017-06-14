from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

class EditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            is_edit_form = kwargs.pop('is_edit_form')
        except KeyError:
            is_edit_form = False
        try:
            cancel_url = kwargs.pop('cancel_url')
        except KeyError:
            cancel_url = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("save record", "Save", css_class='save_butt main-butt'))
        if is_edit_form:
            self.helper.add_input(Submit("delete record", "Delete", css_class='btn btn-danger delete-btn  main-butt'))
        else:
            if cancel_url is not None:
                cancel_onclick = "javascript:location.href = '" + cancel_url + "';"
                self.helper.add_input(Button("cancel add", "Cancel", css_class='btn btn-default cancel-btn main-butt', onclick=cancel_onclick))
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []        # Note: if I use 'disabled' then the post returns nothing for the fields

    class Meta:
        abstract = True

    def prepare_required_field(self, field, label):
        self.fields[field].label = label + '*'
        self.fields[field].required = False
