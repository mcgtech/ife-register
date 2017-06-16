
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# dont check this line in!!
try:
    admin = User.objects.get(pk=1)
except:
    admin = User.objects.create_superuser('admin', 'a@a.com', 'xxx')

admin_group = Group(name="admin")
admin_group.save()
# applicant - ie an engineer who want to be on the register
engineers_group = Group(name="engineer")
engineers_group.save()

# member of institute of fire engineers they decide if engineer is okay to be on register
approver_group = Group(name="approver")
approver_group.save()
approver = User.objects.create_user(username='approver', email="approver@gmail.co.uk",  password="approver123")
approver.is_staff=True
approver.save()
approver_group.user_set.add(approver)
approver_group.save()

verifier_group = Group(name="verifier")
verifier_group.save()
verifier = User.objects.create_user(username='verifier', email="verifier@gmail.co.uk",  password="verifier123")
verifier.save()
verifier_group.user_set.add(verifier)
verifier_group.save()