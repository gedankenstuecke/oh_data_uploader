from django.conf import settings


def read_config(request):
    context = {'yaml_config': settings.YAML_CONFIG,
               'oh_proj_page': settings.YAML_CONFIG['oh_activity_page']}
    return context
