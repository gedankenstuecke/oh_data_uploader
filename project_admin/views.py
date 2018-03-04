from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render

from .models import ProjectConfiguration, FileMetaData
import json

User = get_user_model()


def home(request):
    """
    Main page for project config.
    """
    if request.user.username == 'admin':
        project_config = ProjectConfiguration.objects.get(id=1)
        files = FileMetaData.objects.all()
        for file in files:
            file.tags = ','.join(json.loads(file.tags)) if file.tags else ''
        context = {'project_config': project_config, 'files': files}
        return render(request, 'project_admin/home.html', context=context)
    else:
        return redirect('project-admin:login')


def config(request):
    """
    Edit project config.
    """
    project_config = ProjectConfiguration.objects.get(id=1)
    context = {'project_config': project_config}
    return render(request, 'project_admin/config.html', context=context)


def admin_login(request):
    """
    Log in as project admin.
    """
    if request.method == 'POST':
        if not settings.ADMIN_PASSWORD:
            return render(request, 'project_admin/login.html',
                          context={'error': 'ADMIN_PASSWORD environment '
                                   'variable needs to be set!'})
        elif request.POST['password'] == settings.ADMIN_PASSWORD:
            admin_user = User.objects.get(username='admin')
            login(request, admin_user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('project-admin:home')
        else:
            return render(request, 'project_admin/login.html',
                          context={'error': 'Password incorrect.'})

    return render(request, 'project_admin/login.html')


def config_general_settings(request):
    """
    Update Open Humans project configuration.
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    if request.method == 'POST':
        project_config = ProjectConfiguration.objects.get(id=1)
        project_config.project_title = request.POST['project_title']
        project_config.project_description = request.POST[
            'project_description']
        project_config.more_info_url = request.POST['more_info_url']
        project_config.logo_url = request.POST['logo_url']
        project_config.save()
        return redirect('project-admin:home')

    return render(request, 'project_admin/config-general-settings.html')


def config_oh_settings(request):
    """
    Update Open Humans project configuration.
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    if request.method == 'POST':
        project_config = ProjectConfiguration.objects.get(id=1)
        project_config.oh_client_id = request.POST['client_id']
        project_config.oh_client_secret = request.POST['client_secret']
        project_config.oh_activity_page = request.POST['activity_page']
        project_config.save()
        return redirect('project-admin:home')

    return render(request, 'project_admin/config-oh-settings.html')


def config_file_settings(request):
    """
    Update file metadata settings
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    files = FileMetaData.objects.all()

    if request.method == 'POST':
        for file in files:
            file.name = request.POST["file_{}_name".format(file.id)]
            file.description = request.POST["file_{}_description"
                                            .format(file.id)]
            file.tags = json.dumps(request.POST["file_{}_tags"
                                   .format(file.id)].split(","))
            file.save()
        return redirect('project-admin:home')

    for file in files:
        file.tags = ','.join(json.loads(file.tags)) if file.tags else ''
    context = {"files": files}
    return render(request, 'project_admin/config-file-settings.html',
                  context=context)


def config_homepage_text(request):
    """
    Update Open Humans project configuration.
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    if request.method == 'POST':
        project_config = ProjectConfiguration.objects.get(id=1)
        project_config.homepage_text = request.POST['homepage_text']
        project_config.about = request.POST['about']
        project_config.faq = request.POST['faq']
        project_config.overview = request.POST['overview']
        project_config.upload_description = request.POST['upload_description']
        project_config.save()
        return redirect('project-admin:home')

    return render(request, 'project_admin/config-homepage-text.html')


def add_file(request):
    """
    Add file metadata object
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    if request.method == 'POST':
        files = FileMetaData.objects.all()
        for file in files:
            file.name = request.POST["file_{}_name".format(file.id)]
            file.description = request.POST["file_{}_description"
                                            .format(file.id)]
            file.tags = json.dumps(request.POST["file_{}_tags"
                                   .format(file.id)].split(","))
            file.save()

        file = FileMetaData.objects.create()
        file.name = "File {}".format(file.id)
        file.save()

    return redirect('project-admin:config-file-settings')


def delete_file(request, file_id):
    """
    Delete file metadata object
    """
    if request.user.username != 'admin':
        return redirect('project-admin:home')

    if request.method == 'POST':
        files = FileMetaData.objects.all()
        for file in files:
            file.name = request.POST["file_{}_name".format(file.id)]
            file.description = request.POST["file_{}_description"
                                            .format(file.id)]
            file.tags = json.dumps(request.POST["file_{}_tags"
                                   .format(file.id)].split(","))
            file.save()

        file = FileMetaData.objects.get(id=file_id)
        file.delete()

    return redirect('project-admin:config-file-settings')
