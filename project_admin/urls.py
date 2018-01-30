from django.conf.urls import url

from . import views

app_name = 'project-admin'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^config-oh-settings/?$',
        views.config_oh_settings, name='config-oh-settings'),
    url(r'^login/?$', views.admin_login, name='login'),
]
