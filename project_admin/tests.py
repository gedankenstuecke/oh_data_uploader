from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings


class AdminLoginTestCase(TestCase):
    def setUp(self):
        settings.DEBUG = True
        settings.ADMIN_PASSWORD = 'test1234'
        call_command('init_proj_config')

    def test_admin_login_redirect(self):
        c = Client()
        response = c.get("/project-admin/")
        self.assertRedirects(response, '/project-admin/login')

    def test_admin_login_success(self):
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        self.assertRedirects(response, '/project-admin/')
        self.assertContains(response, "Current Project Configuration")

    def test_admin_login_fail(self):
        c = Client()
        response = c.post("/project-admin/login/", {'password': 'meep'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password incorrect")
