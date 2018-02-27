from django.test import TestCase, Client, RequestFactory
from django.core.management import call_command
from django.conf import settings
from open_humans.models import OpenHumansMember


class LoginTestCase(TestCase):
    def setUp(self):
        settings.DEBUG = True
        call_command('init_proj_config')
        self.factory = RequestFactory()
        self.oh_member = OpenHumansMember.create(oh_id='1234567890abcdef',
                                                 access_token='foo',
                                                 refresh_token='bar',
                                                 expires_in=2000)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_index_logged_out(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_logged_in(self):
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.get("/")
        print(response.content)
        self.assertRedirects(response, '/overview')
