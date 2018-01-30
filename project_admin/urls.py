from django.conf.urls import url

from . import views

app_name = 'project-admin'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^config-general-settings/?$',
        views.config_general_settings, name='config-general-settings'),
    url(r'^config-oh-settings/?$',
        views.config_oh_settings, name='config-oh-settings'),
    url(r'^config-homepage-text/?$',
        views.config_homepage_text, name='config-homepage-text'),
    url(r'^login/?$', views.admin_login, name='login'),
]
