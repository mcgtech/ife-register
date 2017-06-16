from django.conf.urls import url
from . import views
from register.views import *


urlpatterns = [
    url(r'^engineer_signup/$', views.engineer_signup, name='engineer_signup'),
    url(r'^engineer_welcome/$', views.engineer_welcome, name='engineer_welcome'),
    url(r'^engineer_app_edit/(?P<user_pk>\d+)$', views.engineer_applicant_edit, name='engineer_app_edit'),
    url(r'^engineer/new/$', views.engineer_new, name='engineer_new'),
    url(r'^engineer/(?P<pk>\d+)/edit/$', views.engineer_edit, name='engineer_edit'),
    url(r'^engineer_search/$', EngineerViewFilter.as_view(), name='engineer_search'),
]