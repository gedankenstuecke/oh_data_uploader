from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from open_humans.models import OpenHumansMember

# this should trigger the hound.
class OpenHumansMemberTest(TestCase):
    def setUp(self):
        settings.DEBUG = True
        call_command('init_proj_config')
        self.oh_member = OpenHumansMember(oh_id=1234, access_token='foo', refresh_token='bar')

    def tests_str_(self):
        self.assertEqual(str(self.oh_member), "<OpenHumansMember(oh_id='1234')>")
