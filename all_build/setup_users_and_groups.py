
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# dont check this line in!!
User.objects.create_superuser('admin', 'a@a.com', 'xxx')


admin_group = Group(name="admin")
admin_group.save()