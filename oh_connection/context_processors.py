from django.conf import settings


def read_config(request):
    context = {'yaml_config': settings.YAML_CONFIG,
               'oh_proj_page': settings.OH_ACTIVITY_PAGE}
    return context
