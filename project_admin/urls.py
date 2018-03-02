from django.conf.urls import url

from . import views

app_name = 'project-admin'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^config-general-settings/?$',
        views.config_general_settings, name='config-general-settings'),
    url(r'^config-oh-settings/?$',
        views.config_oh_settings, name='config-oh-settings'),
    url(r'^config-file-settings/?$',
        views.config_file_settings, name='config-file-settings'),
    url(r'^config-homepage-text/?$',
        views.config_homepage_text, name='config-homepage-text'),
    url(r'^login/?$', views.admin_login, name='login'),
    url(r'^add-file/?$', views.add_file, name='add-file'),
    url(r'^delete-file/(?P<file_id>\w+)/?$', views.delete_file, name='delete-file'),
]
