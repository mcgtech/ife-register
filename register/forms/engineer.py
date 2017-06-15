from register.models import Engineer, Address, Telephone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField, PrependedText
from common.forms import *

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class EngineerForm(EditForm, AuditableForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
                TabHolder(
                    Tab('Contact Details',
                        Div(Div('title', 'forename', 'middle_name', 'surname', css_class="col-sm-6 name_con"), Div(css_class="col-sm-6 address")),),
                    Tab('Professional Indemnity', PrependedText('pi_insurance_cover', '£'), 'pi_renewal_date', 'pi_company',
                        ),
                    Tab('Experience', 'build_std_know', 'type_of_work',
                        ),
                    Tab(
                        'Log',
                        'created_by',
                        'created_on',
                        'modified_by',
                        'modified_on'
                    ),))

        self.prepare_required_field('title', 'Title')
        self.prepare_required_field('forename', 'Forename')
        self.prepare_required_field('surname', 'Surname')
        self.prepare_required_field('employer', 'Employer')
        class Meta(AuditableForm.Meta):
            model = Engineer
            AuditableForm.Meta.widgets['build_std_know'] = forms.Textarea(attrs={'placeholder': 'Name'})
            AuditableForm.Meta.widgets['type_of_work'] = forms.Textarea(attrs={'placeholder': 'Enter description here'})

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_title(self):
        return validate_required_field(self, 'title', 'title')

    def clean_forename(self):
        return validate_required_field(self, 'forename', 'forename')

    def clean_surname(self):
        return validate_required_field(self, 'surname', 'surname')

    def clean_employer(self):
        return validate_required_field(self, 'employer', 'employer')

    class Meta(AuditableForm.Meta):
        model = Engineer
        fields = get_auditable_fields() + ('title', 'forename', 'middle_name', 'surname', 'employer',
                                           'pi_insurance_cover', 'pi_renewal_date', 'pi_company',
                                           'build_std_know', 'type_of_work')



class AddressForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout('line_1', 'line_2', 'line_3',
                           Div(Div('post_code', css_class="col-sm-6"), Div('post_town', css_class="col-sm-6"), css_class='row postcode'),
                           'country',
                  )
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'line_3','post_code', 'post_town', 'country')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['line_1'].label = "Address line 1*"
        self.fields['post_code'].label = "Postal Code*"
        self.fields['country'].label = "Country*"
        self.fields['line_1'].required = False
        self.fields['post_code'].required = False
        self.fields['country'].required = False

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_line_1(self):
        return validate_required_field(self, 'line_1', 'line 1')

    def clean_post_code(self):
        return validate_required_field(self, 'post_code', 'postal code')

    def clean_country(self):
        return validate_required_field(self, 'country', 'country')


# one to many forms

class PhoneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Telephone
        fields = ('type', 'number', )


class PhoneFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PhoneFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'
