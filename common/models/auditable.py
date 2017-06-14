from django.db import models
from django.conf import settings

class Auditable(models.Model):
    created_on = models.DateTimeField(null=True, blank=True)
    # https://www.webforefront.com/django/setuprelationshipsdjangomodels.html
    # a user may have created many Auditable class objects, but an instance of an Auditable can have only created by,
    # so in django we add the ForeignKey to the many part of the relationship:
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_created_by', blank=True, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    # https://www.webforefront.com/django/setuprelationshipsdjangomodels.html
    # a user may have created many Auditable class objects, but an instance of an
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modified_by', blank=True, null=True)

    class Meta:
        abstract = True
