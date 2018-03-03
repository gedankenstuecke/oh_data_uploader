from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings


class AdminLoginTestCase(TestCase):
    """
    Tests Admin login
    """

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True
        settings.ADMIN_PASSWORD = 'test1234'
        call_command('init_proj_config')

    def test_admin_login_redirect(self):
        """
        Test redirection to the login page
        """
        c = Client()
        response = c.get("/project-admin/")
        self.assertRedirects(response, '/project-admin/login')

    def test_admin_login_success(self):
        """
        Test successful log in attempt.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        self.assertRedirects(response, '/project-admin/')
        self.assertContains(response, "Current Project Configuration")

    def test_admin_login_fail(self):
        """
        Test unsuccessful login attempt.
        """
        c = Client()
        response = c.post("/project-admin/login/", {'password': 'meep'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password incorrect")

    def test_config_homepage_text_logged_out(self):
        """
        Test config_homepage_text function when logged out
        """
        c = Client()
        response = c.get("/project-admin/config-homepage-text/")
        self.assertEqual(response.status_code, 302)

    def test_get_config_homepage_text(self):
        """
        Test making a get request to
        config_homepage_text function when logged in.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.get("/project-admin/config-homepage-text/")
        self.assertIn('<i>Github</i> has a <a href="https://guides'
                      '.github.com/features/mastering-markdown/#syntax">',
                      str(response.content))

    def test_post_config_homepage_text(self):
        """
        Test making a post request to
        config_homepage_text function when logged in.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.post("/project-admin/config-homepage-text/",
                          {'faq': 'foo',
                           'about': 'bar',
                           'overview': 'foo-bar',
                           'homepage_text': 'foobar!',
                           'upload_description': 'foo_bar'},
                          follow=True)
        self.assertEqual(response.context['config'].faq, 'foo')
        self.assertEqual(response.context['config'].about, 'bar')
        self.assertEqual(response.context['config'].overview, 'foo-bar')
        self.assertEqual(response.context['config'].homepage_text, 'foobar!')
        self.assertEqual(response.context['config'].upload_description,
                         'foo_bar')
