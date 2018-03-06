"""
Create your tests here.
"""
import vcr
from django.test import TestCase
from main.views import delete_all_oh_files
from open_humans.models import OpenHumansMember
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command


class DeleteTests(TestCase):
    def setUp(self):
        settings.DEBUG = True
        call_command('init_proj_config')
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        self.oh_member = OpenHumansMember.create(oh_id=1234,
                                                 data=data)
        self.user = User(username='user1')
        self.user.save()

    @vcr.use_cassette('main/tests/fixtures/delete_all.yaml',
                      record_mode='none')
    def test_delete_all(self):
        delete_all_oh_files(self.oh_member)
