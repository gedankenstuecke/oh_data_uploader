from django.test import TestCase, Client, RequestFactory
from django.core.management import call_command
from django.conf import settings
from open_humans.models import OpenHumansMember
from main.views import upload_file_to_oh
import requests_mock

OH_BASE_URL = settings.OPENHUMANS_OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_OAUTH2_REDIRECT_URI = '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL)


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
        self.assertRedirects(response, '/overview')

    def test_upload_function(self):
        with requests_mock.Mocker() as m:
            # API-upload-URL
            upload_url = '{}?access_token={}'.format(
                OH_DIRECT_UPLOAD, self.oh_member.access_token)
            # mock delete-API call
            m.register_uri('POST',
                           OH_API_BASE+"/project/files/delete/",
                           status_code=200)
            # mock request 1 to initiate upload, get AWS link
            m.register_uri('POST',
                           upload_url,
                           json={'url':
                                 'http://example.com/upload',
                                 'id': 1234},
                           status_code=201)
            # mock AWS link
            m.register_uri('PUT',
                           'http://example.com/upload',
                           status_code=200)
            # mock completed link
            m.register_uri('POST',
                           OH_DIRECT_UPLOAD_COMPLETE,
                           status_code=200)

            upload_file_to_oh(self.oh_member,
                              open("README.md"),
                              {'tags': '["foo"]'})
