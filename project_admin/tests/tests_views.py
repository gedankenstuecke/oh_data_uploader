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
        self.assertTemplateUsed(response, 'project_admin/home.html')

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
        self.assertRedirects(response, '/project-admin/',
                             status_code=302, target_status_code=302)

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'project_admin/config-homepage-text.html')

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

    def test_config_file_settings_logged_out(self):
        """
        Test config_file_settings function when logged out
        """
        c = Client()
        response = c.get("/project-admin/config-file-settings/")
        self.assertRedirects(response, '/project-admin/',
                             status_code=302, target_status_code=302)

    def test_post_config_file_settings(self):
        """
        Test making a post request to
        config_file_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.post("/project-admin/config-file-settings/",
                          {'file_description': 'foo',
                           'file_tags': 'foo,bar', },
                          follow=True)
        self.assertEqual(response.context['config'].file_description, 'foo')
        self.assertEqual(response.context['config'].file_tags,
                         '["foo", "bar"]')

    def test_get_config_file_settings(self):
        """
        Test making a get request to
        config_file_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.get("/project-admin/config-file-settings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'project_admin/config-file-settings.html')

    def test_config_oh_settings_logged_out(self):
        """
        Test config_oh_settings function when logged out
        """
        c = Client()
        response = c.get("/project-admin/config-oh-settings/")
        self.assertRedirects(response, '/project-admin/',
                             status_code=302, target_status_code=302)

    def test_post_config_oh_settings(self):
        """
        Test making a post request to
        config_oh_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.post("/project-admin/config-oh-settings/",
                          {'client_id': 'foo',
                           'client_secret': 'foobar',
                           'activity_page': 'foo-bar'},
                          follow=True)
        self.assertEqual(response.context['config'].oh_client_id, 'foo')
        self.assertEqual(response.context['config'].oh_client_secret,
                         'foobar')
        self.assertEqual(response.context['config'].oh_activity_page,
                         'foo-bar')

    def test_get_config_oh_settings(self):
        """
        Test making a get request to
        config_oh_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.get("/project-admin/config-oh-settings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'project_admin/config-oh-settings.html')

    def test_config_general_settings_logged_out(self):
        """
        Test config_general_settings function when logged out
        """
        c = Client()
        response = c.get("/project-admin/config-general-settings/")
        self.assertRedirects(response, '/project-admin/',
                             status_code=302, target_status_code=302)

    def test_post_config_general_settings(self):
        """
        Test making a post request to
        config_general_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.post("/project-admin/config-general-settings/",
                          {'project_title': 'foo',
                           'project_description': 'foobar',
                           'more_info_url': 'www.foo-bar.com',
                           'logo_url': 'www.foobar.com'},
                          follow=True)
        self.assertEqual(response.context['config'].project_title, 'foo')
        self.assertEqual(response.context['config'].project_description,
                         'foobar')
        self.assertEqual(response.context['config'].more_info_url,
                         'www.foo-bar.com')
        self.assertEqual(response.context['config'].logo_url,
                         'www.foobar.com')

    def test_get_config_general_settings(self):
        """
        Test making a get request to
        config_general_settings.
        """
        c = Client()
        response = c.post("/project-admin/login/",
                          {'password': 'test1234'},
                          follow=True)
        response = c.get("/project-admin/config-general-settings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'project_admin/config-general-settings.html')
