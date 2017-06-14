from django.conf.urls import url
from . import views
from register.views import *


urlpatterns = [
    url(r'^engineer/new/$', views.engineer_new, name='engineer_new'),
    url(r'^engineer/(?P<pk>\d+)/edit/$', views.engineer_edit, name='engineer_edit'),
    url(r'^engineer_search/$', EngineerViewFilter.as_view(), name='engineer_search'),
]