from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
import markdown


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
