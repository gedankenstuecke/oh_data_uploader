from django.test import TestCase, Client, RequestFactory
from django.core.management import call_command
from django.conf import settings
from open_humans.models import OpenHumansMember
from main.views import upload_file_to_oh
import requests_mock
from unittest.mock import mock_open, patch
from main.templatetags.utilities import concatenate
from main.helpers import get_create_member
import vcr

OH_BASE_URL = settings.OPENHUMANS_OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_OAUTH2_REDIRECT_URI = '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL)
OH_GET_URL = OH_API_BASE + '/project/exchange-member/'


class LoginTestCase(TestCase):
    """
    Tests for index page and upload feature
    """

    def setUp(self):
        """
        Set up the app for following tests
        """
        settings.DEBUG = True
        call_command('init_proj_config')
        self.factory = RequestFactory()
        self.oh_member = OpenHumansMember.create(oh_id='12345678',
                                                 access_token='foo',
                                                 refresh_token='bar',
                                                 expires_in=2000)
        self.oh_member.save()
        self.user = self.oh_member.user
        self.user.set_password('foobar')
        self.user.save()

    def test_index_logged_out(self):
        """
        Test index page when logged out
        """
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_logged_in(self):
        """
        Test if redirection happens when user logs in.
        """
        c = Client()
        c.login(username=self.user.username, password='foobar')
        response = c.get("/")
        self.assertRedirects(response, '/overview')

    def test_upload_function(self):
        """
        Tests upload feature
        """
        with requests_mock.Mocker() as m:
            # API-upload-URL
            upload_url = '{}?access_token={}'.format(
                OH_DIRECT_UPLOAD, self.oh_member.access_token)
            # mock delete-API call
            m.register_uri('POST',
                           OH_API_BASE + "/project/files/delete/",
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
            with patch('builtins.open',
                       mock_open(read_data='foobar'),
                       create=True):
                fake_file = open('foo')
                upload_file_to_oh(self.oh_member,
                                  fake_file,
                                  {'tags': '["foo"]'})

    def test_list_files(self):
        """
        Test the list_files function.
        """
        with requests_mock.Mocker() as m:
            get_url = '{}?access_token={}'.format(
                OH_GET_URL, self.oh_member.access_token)
            m.register_uri('GET',
                           get_url,
                           json={'data': [
                            {'id': '1',
                             'basename': 'foo',
                             'download_url': 'www.foobar.com',
                             'metadata': {
                                          'description': '',
                                          'tags': '["foo"]',
                                          },
                             }]
                           },
                           status_code=200)
            c = Client()
            c.login(username=self.user.username, password='foobar')
            data = c.get("/list")
            self.assertEqual(data.status_code, 200)
            self.assertIn('<a href="www.foobar.com"', str(data.content))

    def test_list_files_logged_out(self):
        """
        Test the list_files function when logged out.
        """
        c = Client()
        response = c.get("/list")
        self.assertRedirects(response, '/')

    def test_concatenate(self):
        """
        Test concatenate template function
        """
        self.assertEqual(concatenate("a", "b", "c"), "a_b_c")

    @vcr.use_cassette('main/tests/fixtures/token_exchange_valid.yaml',
                      record_mode='none')
    def test_get_create(self):
        """
        Test get/create helper get_create helper
        """
        self.assertEqual(1,
                         OpenHumansMember.objects.all().count())
        data = {'access_token': 'returnedaccesstoken',
                'refresh_token': 'refreshed_token',
                'expires_in': 36000}
        oh_member = get_create_member(data)
        self.assertEqual(1,
                         OpenHumansMember.objects.all().count())
