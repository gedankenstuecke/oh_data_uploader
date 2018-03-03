from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings


class User_Views_Test( TestCase ):

    def setUp( self ):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True
        settings.ADMIN_PASSWORD = '123'
        call_command( 'init_proj_config' )

    def test_project_config_view(self):
        response = self.client.get( "/project-admin/" )
        self.assertRedirects( response, '/project-admin/login' )
        self.assertEqual( response.status_code, 302 )

    def test_project_config_page_returns_correct_html(self):
        c = Client()
        response = c.post( "/project-admin/login", {'user': 'admin', 'password': '123'}, follow=True )
        self.assertContains( response, '<h1>Current Project Configuration</h1>', status_code=200 )
        self.assertTemplateUsed( response, 'project_admin/home.html' )
