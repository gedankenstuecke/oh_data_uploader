from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render

from .models import ProjectConfiguration

User = get_user_model()


def home(request):
    """
    Main page for project config.
    """
    if request.user.username == 'admin':
        project_config = ProjectConfiguration.objects.get(id=1)
        context = {'project_config': project_config}
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
