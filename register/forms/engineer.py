from register.models import Engineer, Address, Telephone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField, PrependedText
from common.forms import *
from common.views.authentication import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class EngineerForm(EditForm, AuditableForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        con_dets_help = '<p>Please let us know how we can contact you.</p>'
        con_dets_help += '<p>When you are done here work through the other tabs to finish your application.</p>'
        con_dets_help += '<p>Click submit when you are done.</p>'
        con_dets_help = get_help_markup(con_dets_help)
        exp_help = '<p>Tell us little about your experience before moving on to the next tab.</p>'
        exp_help += '<p>You can go back and change details on any tab at any point before you submit your application, but we would appreciate it if you can fill in as much information as possible.</p>'
        exp_help = get_help_markup(exp_help)
        int_help = '<p>Enter details of all relevant professional bodies that you are an active member of.</p>'
        int_help = get_help_markup(int_help)
        pi_help = '<p>Okay nearly there, let us know the details if you have current Professional Indemnity (PI) insurance.</p>'
        pi_help += '<p>Once you are done simply click Submit and then we will be in touch.</p>'
        pi_help = get_help_markup(pi_help)

        self.helper.layout = Layout(
                TabHolder(
                    Tab('1. About You',
                        HTML(con_dets_help),
                        # Div(Div('title', 'forename', 'middle_name', 'surname', css_class="col-sm-6 name_con"), Div(css_class="col-sm-6 address")),),
                        Div(Div('title', 'middle_name', css_class="col-sm-6 name_con"), Div(css_class="col-sm-6 address")),),
                    Tab('2. Experience', HTML(exp_help), 'employer', 'build_std_know', 'type_of_work',
                        ),
                    Tab('3. Institution Membership',
                        HTML(int_help),
                        Div(
                            Div(Fieldset('IFE', 'ife_member_grade', 'ife_member_no', 'ife_member_reg_date', css_class="ife"), css_class="col-sm-6"),
                            Div(Fieldset('Engineering Council', 'ec_member_grade', 'ec_member_no', 'ec_member_reg_date',css_class="ec"), css_class="col-sm-6")
                        ),
                        Div(
                            Div(Fieldset('Other Institution', 'other_inst', 'other_inst_no', 'other_inst_reg_date', css_class="oi"), css_class="col-sm-6"),
                            Div(Fieldset('Additional Information', 'add_mem', 'cpd', css_class="ai"), css_class="col-sm-6") ,
                        )),
                    Tab('4. Professional Indemnity', HTML(pi_help),
                        Div(
                            Div(PrependedText('pi_insurance_cover', get_base_ccy_prefix()), 'pi_renewal_date', css_class="col-sm-6"),
                            Div('pi_company', css_class="col-sm-6")),
                        ),
                    Tab(
                        'Log',
                        'created_by',
                        'created_on',
                        'modified_by',
                        'modified_on'
                    ),))
        self.prepare_required_field('title', 'Title')
        # self.prepare_required_field('forename', 'Forename')
        # self.prepare_required_field('surname', 'Surname')
        self.fields['pi_insurance_cover'].required = False
        self.fields['ife_member_grade'].required = False
        self.fields['ec_member_grade'].required = False

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_title(self):
        return validate_required_field(self, 'title', 'title')

    # def clean_forename(self):
    #     return validate_required_field(self, 'forename', 'forename')
    #
    # def clean_surname(self):
    #     return validate_required_field(self, 'surname', 'surname')

    class Meta(AuditableForm.Meta):
        model = Engineer
        fields = get_auditable_fields() + ('title',
                                           # 'forename', 'surname',
                                           'middle_name', 'employer',
                                           'pi_insurance_cover', 'pi_renewal_date', 'pi_company',
                                           'build_std_know', 'type_of_work',
                                           'ife_member_grade', 'ife_member_no', 'ife_member_reg_date',
                                           'ec_member_grade', 'ec_member_no', 'ec_member_reg_date',
                                           'other_inst', 'other_inst_no', 'other_inst_reg_date',
                                           'add_mem', 'cpd')
        AuditableForm.Meta.widgets['build_std_know'] = forms.Textarea(attrs={'placeholder': 'Enter details of your current knowledge of the Scottish Building Standards system'})
        AuditableForm.Meta.widgets['employer'] = forms.TextInput(attrs={'placeholder': 'Current employers name'})
        AuditableForm.Meta.widgets['type_of_work'] = forms.Textarea(attrs={'placeholder': 'e.g. fire engineering design, Computational Fluid Dynamics (CFD), fire engineering regulator, structural fire engineering, smoke control specialist etc'})
        AuditableForm.Meta.widgets['add_mem'] = forms.Textarea(attrs={'placeholder': 'Please tell us about an other relevant professional bodies that you are a member of'})
        AuditableForm.Meta.widgets['other_inst'] = forms.Textarea(attrs={'placeholder': 'Please tell us about an other relevant institutions that you are a member of'})
        AuditableForm.Meta.widgets['cpd'] = forms.Textarea(attrs={'placeholder': 'Continuing professional development (CPD) is a way for you to show that you are committed to learning and developing throughout your career. Please detail your CPD for the past year and your plans for the year ahead'})
        AuditableForm.Meta.widgets['pi_renewal_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['ife_member_reg_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['ec_member_reg_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['other_inst_reg_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['pi_company'] = forms.Textarea(attrs={'rows':4})



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

def get_help_markup(text):
    markup = '<div class ="alert alert-info alert-dismissible" role="alert">'
    markup += text
    markup += '</div>'

    return markup