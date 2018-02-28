from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
import markdown

class AboutPageTestCase(TestCase):

	def setUp(self):
		settings.DEBUG = True
		call_command('init_proj_config')

	def test_about_page(self):
		c = Client()
		response = c.get('/about')
		self.assertEqual(response.status_code, 200)

	def test_about_page_content(self):
		c = Client()
		response = c.get('/about')
		with open('_descriptions/about.md', 'r') as f: 
			content_file = f.readlines()
		content = ""
		for i in range(len(content_file)):
			content += str(content_file[i])
		self.assertIn(markdown.markdown(content).encode(), response.content)



