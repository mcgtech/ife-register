
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# dont check this line in!!
User.objects.create_superuser('admin', 'a@a.com', 'xxx')


admin_group = Group(name="admin")
admin_group.save()
# applicant - ie an engineer who want to be on the register
engineers_group = Group(name="engineer")
engineers_group.save()
# member of institute of fire engineers they decide if engineer is okay to be on register
approver_group = Group(name="approver")
approver_group.save()
# they will search for engineer on the site to see if they can be allowed to do some work
approver_group = Group(name="verifier")
approver_group.save()