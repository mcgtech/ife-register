from django.db import models
from common.models import Auditable
from django_countries.fields import CountryField

# see https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# to see how I attach associate person with address
class Address(models.Model):
    line_1 = models.CharField(max_length=200)
    line_2 = models.CharField(max_length=200, blank=True)
    line_3 = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=100)
    post_town = models.CharField(max_length=100, blank=True)
    country = CountryField(default='GB')

    def __str__(self):
        add = []
        if len(self.line_1.strip()):
            add.append(self.line_1.strip())
        if len(self.line_2.strip()):
            add.append(self.line_2.strip())
        if len(self.line_3.strip()):
            add.append(self.line_3.strip())

        return ", ".join(add)


class Engineer(Auditable):
    MR = 0
    MRS = 1
    MISS = 2
    MS = 3
    TITLES = (
        (None, 'Please select'),
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MISS, 'Miss'),
        (MS, 'Ms'),
    )
    title = models.IntegerField(choices=TITLES, default=None)
    middle_name = models.CharField(max_length=100, blank=True)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    employer = models.CharField(max_length=200)
    address = models.OneToOneField(Address, null=True, related_name="engineer", on_delete=models.SET_NULL)
    # ins
    pi_insurance_cover = models.FloatField(default=0.0, verbose_name='Annual cover')
    pi_renewal_date = models.DateField(null=True, blank=True, verbose_name='Renewal date')
    pi_company = models.CharField(max_length=100, blank=True, verbose_name='Insurance company')
    # experience
    build_std_know = models.TextField(blank=True, verbose_name='Knowledge of Scottish Building Standards system')
    type_of_work = models.TextField(blank=True, verbose_name='Type of work undertaken')
    # official body
    # IFE
    IFE_TECH = 0
    IFE_GRAD = 1
    IFE_ASSOC = 2
    IFE_MEM = 3
    IFE_FELL = 4
    IFE_GRADES = (
        (None, 'Please select'),
        (IFE_TECH, 'Technician (TIFireE)'),
        (IFE_GRAD, 'Graduate (GIFireE)'),
        (IFE_ASSOC, 'Associate (AIFireE)'),
        (IFE_MEM, 'Member (MIFireE)'),
        (IFE_FELL, 'Fellow (FIFireE)'),
    )
    ife_member_grade = models.IntegerField(choices=IFE_GRADES, default=None, verbose_name='membership grade')
    ife_member_no = models.CharField(max_length=100, blank=True, verbose_name='membership number')
    ife_member_reg_date = models.DateField(null=True, blank=True, verbose_name='registration date')
    # Engineering Council
    # IFE
    EC_AFF = 0
    EC_STUD = 1
    EC_GRAD = 2
    EC_LIC = 3
    EC_ASSOC = 4
    EC_MEM = 4
    EC_FELL = 4
    ENG_COUN_GRADES = (
        (None, 'Please select'),
        (EC_AFF, 'Affiliate'),
        (EC_STUD, 'Student'),
        (EC_GRAD, 'Graduate'),
        (EC_LIC, 'Licentate'),
        (EC_ASSOC, 'Associate'),
        (EC_MEM, 'Member'),
        (EC_FELL, 'Fellow'),
    )
    ec_member_grade = models.IntegerField(choices=ENG_COUN_GRADES, default=None, verbose_name='council grade')
    ec_member_no = models.CharField(max_length=100, verbose_name='council number')
    ec_member_reg_date = models.DateField(null=True, blank=True, verbose_name='registration date')
    # other
    other_inst = models.TextField(blank=True, verbose_name='other institutions')
    other_inst_no = models.CharField(max_length=100, verbose_name='membership number')
    other_inst_reg_date = models.DateField(null=True, blank=True, verbose_name='registration date')
    # add mem
    add_mem = models.TextField(blank=True, verbose_name='Additional memberships')
    # cpd
    cpd = models.TextField(blank=True, verbose_name='Continual Professional Development')

    def get_full_name(self):
        full_name = self.get_title_display
        if self.middle_name is not None and len(self.forename):
            full_name = ' ' + self.forename
        if self.middle_name is not None and len(self.middle_name):
            full_name = full_name + ' ' + self.middle_name
        if self.surname is not None and len(self.surname):
            full_name = full_name + ' ' + self.surname

        return full_name

    def __str__(self):
        return self.get_full_name()


class Telephone(models.Model):
    HOME = 0
    MOBILE = 1
    PARENTS = 2
    WORK = 3
    PHONE_TYPES = (
        (None, 'Please select'),
        (HOME, 'Home'),
        (MOBILE, 'Mobile'),
        (WORK, 'Work'),
    )
    type = models.IntegerField(choices=PHONE_TYPES, default=None)
    number = models.CharField(max_length=100, blank=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True, related_name="telephone")

    def __str__(self):
       return self.number + ' (' + self.get_type_display() + ')'