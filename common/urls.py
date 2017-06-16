from django.conf.urls import include, url
from common import views

urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success')
]
