from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from open_humans.models import OpenHumansMember, make_unique_username
from django.contrib.auth.models import User


class OpenHumansMemberTest(TestCase):
    def setUp(self):
        settings.DEBUG = True
        call_command('init_proj_config')
        self.oh_member = OpenHumansMember(oh_id=1234,
                                          access_token='foo',
                                          refresh_token='bar')
        self.user = User(username='user1')
        self.user.save()

    def tests_str_(self):
        self.assertEqual(str(self.oh_member),
                         "<OpenHumansMember(oh_id='1234')>")

    def tests_unique(self):
        self.assertEqual(make_unique_username("user1"),
                         "user12")
