from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from project_admin.models import ProjectConfiguration, FileMetaData
from open_humans.models import OpenHumansMember
import markdown
import vcr
import json
from io import BytesIO


class AboutPageTestCase(TestCase):
    """
    Test cases for the about page.
    """

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True
        call_command('init_proj_config')

    def test_about_page(self):
        """
        Makes request to the about page.
        """
        c = Client()
        response = c.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_about_page_content(self):
        """
        Test whether content is rendered properly.
        """
        c = Client()
        response = c.get('/about')
        with open('_descriptions/about.md', 'r') as f:
            content_file = f.readlines()
        content = ""
        for i in range(len(content_file)):
            content += str(content_file[i])
        self.assertIn(markdown.markdown(content).encode(), response.content)


class IndexPageTestCase(TestCase):
    """
    Test cases for the index page.
    """

    def setUp(self):
        """
        Set up the app for following tests.
        """
        settings.DEBUG = True
        call_command('init_proj_config')

    def test_index_page_content(self):
        """
        Test whether content is rendered properly.
        """
        c = Client()
        response = c.get('/')
        with open('_descriptions/index.md', 'r') as f:
            content_file = f.readlines()
        content = ""
        for i in range(len(content_file)):
            content += str(content_file[i])
        self.assertIn(markdown.markdown(content).encode(), response.content)


class LoginTestCase(TestCase):
    """
    Test the login logic of the OH API
    """

    def setUp(self):
        settings.DEBUG = True
        settings.OPENHUMANS_APP_BASE_URL = "http://127.0.0.1"
        call_command('init_proj_config')
        project_config = ProjectConfiguration.objects.get(id=1)
        project_config.oh_client_id = "6yNYmUlXN1wLwQFQR0lnUohR1KMeVt"
        project_config.oh_client_secret = "Y2xpZW50aWQ6Y2xpZW50c2VjcmV0"
        project_config.save()

    @vcr.use_cassette('main/tests/fixtures/token_exchange_valid.yaml',
                      record_mode='none')
    def test_complete(self):
        c = Client()
        self.assertEqual(0,
                         OpenHumansMember.objects.all().count())
        response = c.get("/complete", {'code': 'mytestcode'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/complete.html')
        self.assertEqual(1,
                         OpenHumansMember.objects.all().count())

    def test_log_out_logged_out(self):
        """
        Tests logout function
        """
        c = Client()
        response = c.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_overview_logged_out(self):
        """
        Tests overview function when logged out
        """
        c = Client()
        response = c.get("/overview")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_log_out(self):
        """
        Tests logout function
        """
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.post('/logout')
        self.assertEqual(response.wsgi_request.user.username, '')
        self.assertRedirects(response, "/")

    def test_delete_single_logged_out(self):
        c = Client()
        response = c.get("/delete/1")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    @vcr.use_cassette('main/tests/fixtures/delete_single.yaml',
                      record_mode='none')
    def test_delete_single(self):
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()
        c = Client()
        c.login(username=self.user.username, password='foobar')

        response = c.get("/delete/1337", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/list.html')


class UploadTestCase(TestCase):
    def setUp(self):
        # set up project
        settings.DEBUG = True
        # settings.OPENHUMANS_APP_BASE_URL = "http://127.0.0.1"
        call_command('init_proj_config')
        project_config = ProjectConfiguration.objects.get(id=1)
        project_config.oh_client_id = "6yNYmUlXN1wLwQFQR0lnUohR1KMeVt"
        project_config.oh_client_secret = "Y2xpZW50aWQ6Y2xpZW50c2VjcmV0"
        project_config.save()

        self.oh_file = FileMetaData()
        self.oh_file.name = "test"
        self.oh_file.description = 'a test file'
        self.oh_file.tags = json.dumps("my,tag,list")
        self.oh_file.save()

        # set up user
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 data=data)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_get_upload_old(self):
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.get("/upload_simple/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "a test file")
        self.assertTemplateUsed(response, 'main/upload_old.html')

    def test_upload_old_logged_out(self):
        c = Client()
        response = c.get("/upload_simple/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    @vcr.use_cassette('main/tests/fixtures/upload_file.yaml',
                      record_mode='none')
    def test_post_upload_old(self):
        c = Client()
        c.login(username=self.user.username, password='foobar')
        test_file = BytesIO(b'mybinarydata')
        test_file.name = 'myimage.jpg'
        response = c.post("/complete/",
                          {'file_1': test_file},
                          follow=True)
        self.assertRedirects(response,
                             "/overview",
                             status_code=302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/overview.html')
