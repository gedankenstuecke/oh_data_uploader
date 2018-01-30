from project_admin.models import ProjectConfiguration

config = ProjectConfiguration.objects.get(id=1)


def read_config(request):
    context = {'config': config,
               'is_admin': request.user.username == 'admin',
               'oh_proj_page': config.oh_activity_page}
    return context
