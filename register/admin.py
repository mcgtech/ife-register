from django.contrib import admin
from .models import Engineer, Telephone, ApplicationStatus

admin.site.register(Engineer)
admin.site.register(ApplicationStatus)
admin.site.register(Telephone)