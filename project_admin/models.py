import json

from django.core.exceptions import ValidationError
from django.db import models


class ProjectConfiguration(models.Model):
    """
    Store project configuration.
    """
    project_title = models.CharField(
        max_length=50,
        default='My Open Humans Project')
    oh_client_id = models.CharField(
        max_length=40,
        blank=True)
    oh_client_secret = models.CharField(
        max_length=128,
        blank=True)

    project_description = models.TextField(
        default='This template demonstrates how you can run your own Open '
                'Humans data upload project.',
        help_text='Project description, displayed on the front page.')
    oh_activity_page = models.TextField(
        help_text='The URL where we can find your project in Open Humans.',
        blank=True)
    file_description = models.TextField(
        help_text='Description of the type of data being uploaded.',
        default="This is an example file that does not have any meaning.")
    file_tags = models.TextField(
        help_text='List of tags that describe file uploads, stored as a '
                  'JSON-formatted array',
        default=json.dumps(['tags', 'are a good way to',
                            'describe the files you are uploading']))
    logo_url = models.TextField(
        blank=True,
        help_text='URL with logo of your project. If left blank, '
                  '/static/default_logo.png will be used.')
    more_info_url = models.TextField(
        blank=True,
        help_text='URL to find more information about your project.')

    about = models.TextField(blank=True)
    faq = models.TextField(blank=True)
    homepage_text = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    upload_description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if ProjectConfiguration.objects.exists() and not self.pk:
            raise ValidationError('Only one ProjectConfiguration allowed')
        return super(ProjectConfiguration, self).save(*args, **kwargs)
