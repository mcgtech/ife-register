"""client_man URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy
from common import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change

#https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name='ife_register_login'),
    url(r'^accounts/logout/$', logout, {'next_page': reverse_lazy('home_page')}, name='ife_register_logout'),
    url(r'^accounts/password_change/$', password_change, {'template_name': 'change_password.html'}, name='password_change'),
    url(r'^accounts/password_reset/$', password_reset, {'template_name': 'password_reset_form.html'}, name='password_reset'),
    url(r'^accounts/password_reset/done/$', password_reset_done, {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', password_reset_complete, {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('common.urls')),
    url(r'', include('register.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)