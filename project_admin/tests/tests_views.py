from django.test import TestCase, Client
from django.http import HttpRequest
from django.core.management import call_command
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string


class ProjectConfig_Views_Test(TestCase):

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True
        settings.ADMIN_PASSWORD = '123'
        call_command('init_proj_config')

    def test_home_view(self):
        user_login = self.client.login(password="123")
        response = self.client.get("/project-admin/")
        self.assertEqual(response.status_code, 302)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        c=Client()
        response = c.post("/project-admin/",{'user':'admin','password':'123'},follow=True)
        self.assertContains( response, '<h1>Current Project Configuration</h1>', status_code=200, html=True )
        self.assertTemplateUsed( response, 'project_admin/home.html' )
        