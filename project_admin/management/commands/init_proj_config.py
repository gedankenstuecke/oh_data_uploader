from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from project_admin.models import ProjectConfiguration

User = get_user_model()


class Command(BaseCommand):
    help = 'Initializes or re-initializes data in ProjectConfiguration.'

    def load_md_text(self, filename):
        return ''.join(
            open('_descriptions/{}'.format(filename), 'r').readlines())

    def handle(self, *args, **options):
        config, _ = ProjectConfiguration.objects.get_or_create(id=1)

        config.about = self.load_md_text('about.md')
        config.homepage_text = self.load_md_text('index.md')
        config.faq = self.load_md_text('faq.md')
        config.overview = self.load_md_text('overview.md')
        config.upload_description = self.load_md_text('upload_description.md')

        config.save()

        User.objects.get_or_create(username='admin')
