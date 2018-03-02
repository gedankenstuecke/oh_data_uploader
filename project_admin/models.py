from django.core.exceptions import ValidationError
from django.db import models


class ProjectConfiguration(models.Model):
    """
    Store project configuration.
    """
    project_title = models.CharField(
        max_length=50,
        blank=True)
    oh_client_id = models.CharField(
        max_length=40,
        blank=True)
    oh_client_secret = models.CharField(
        max_length=128,
        blank=True)

    project_description = models.TextField(
        help_text='Project description, displayed on the front page.',
        blank=True)
    oh_activity_page = models.TextField(
        help_text='The URL where we can find your project in Open Humans.',
        blank=True)
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

    @property
    def client_info(self):
        return {'client_id': self.oh_client_id,
                'client_secret': self.oh_client_secret}

    def save(self, *args, **kwargs):
        if ProjectConfiguration.objects.exists() and not self.pk:
            raise ValidationError('Only one ProjectConfiguration allowed')
        return super(ProjectConfiguration, self).save(*args, **kwargs)


class FileMetaData(models.Model):
    """
    Store file metadata
    """
    name = models.TextField(
        help_text='Name of the file (for representational purposes in the project)'
    )
    description = models.TextField(
        help_text='Description of the type of data being uploaded.',
        blank=True)
    tags = models.TextField(
        help_text='List of tags that describe file uploads, stored as a '
                  'JSON-formatted array',
        blank=True)
