from django.conf.urls import url

from . import views

app_name = 'project-admin'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^config/?$', views.config, name='config'),
]
