from django.shortcuts import render

from .models import ProjectConfiguration


def home(request):
    """
    Main page for project config.
    """
    project_config = ProjectConfiguration.objects.get(id=1)
    context = {'project_config': project_config}
    return render(request, 'project_admin/home.html', context=context)


def config(request):
    """
    Edit project config.
    """
    project_config = ProjectConfiguration.objects.get(id=1)
    context = {'project_config': project_config}
    return render(request, 'project_admin/config.html', context=context)
