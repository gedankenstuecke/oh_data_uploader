import json
import logging
try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError

from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

import ohapi
import requests

from open_humans.models import OpenHumansMember
from project_admin.models import ProjectConfiguration

from .forms import UploadFileForm
logger = logging.getLogger(__name__)

OH_BASE_URL = settings.OPENHUMANS_OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'

OH_OAUTH2_REDIRECT_URI = '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL)


def oh_code_to_member(code):
    """
    Exchange code for token, use this to create and return OpenHumansMember.
    If a matching OpenHumansMember already exists in db, update and return it.
    """
    proj_config = ProjectConfiguration.objects.get(id=1)
    if not (proj_config.oh_client_secret and
            proj_config.oh_client_id and code):
        logger.error('OH_CLIENT_SECRET or code are unavailable')
        return None

    data = ohapi.api.oauth2_token_exchange(
        client_id=proj_config.oh_client_id,
        client_secret=proj_config.oh_client_secret,
        code=code,
        redirect_uri=OH_OAUTH2_REDIRECT_URI,
        base_url=OH_BASE_URL)

    if 'error' in data:
        logger.debug('Error in token exchange: {}'.format(data))
        return None

    if 'access_token' in data:
        oh_id = ohapi.api.exchange_oauth2_member(
            access_token=data['access_token'])['project_member_id']
        try:
            oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
            logger.debug('Member {} re-authorized.'.format(oh_id))
            oh_member.access_token = data['access_token']
            oh_member.refresh_token = data['refresh_token']
            oh_member.token_expires = OpenHumansMember.get_expiration(
                data['expires_in'])
        except OpenHumansMember.DoesNotExist:
            oh_member = OpenHumansMember.create(
                oh_id=oh_id,
                access_token=data['access_token'],
                refresh_token=data['refresh_token'],
                expires_in=data['expires_in'])
            logger.debug('Member {} created.'.format(oh_id))
        oh_member.save()

        return oh_member
    else:
        logger.warning('Neither token nor error info in OH response!')
        return None


def delete_file(request, file_id):
    """
    Delete specified file in Open Humans for this project member.
    """
    if request.user.is_authenticated and request.user.username != 'admin':
        oh_member = request.user.openhumansmember
        client_info = ProjectConfiguration.objects.get(id=1).client_info
        ohapi.api.delete_files(
            project_member_id=oh_member.oh_id,
            access_token=oh_member.get_access_token(**client_info),
            file_id=file_id)
        return redirect('list')
    return redirect('index')


def delete_all_oh_files(oh_member):
    """
    Delete all current project files in Open Humans for this project member.
    """
    client_info = ProjectConfiguration.objects.get(id=1).client_info
    ohapi.api.delete_files(
        project_member_id=oh_member.oh_id,
        access_token=oh_member.get_access_token(**client_info),
        all_files=True)


def upload_file_to_oh(oh_member, filehandle, metadata):
    """
    This demonstrates using the Open Humans "large file" upload process.
    The small file upload process is simpler, but it can time out. This
    alternate approach is required for large files, and still appropriate
    for small files.
    This process is "direct to S3" using three steps: 1. get S3 target URL from
    Open Humans, 2. Perform the upload, 3. Notify Open Humans when complete.
    """
    # Remove any previous file - replace with this one.
    client_info = ProjectConfiguration.objects.get(id=1).client_info

    ohapi.api.delete_files(
        project_member_id=oh_member.oh_id,
        access_token=oh_member.get_access_token(**client_info),
        all_files=True)

    # Get the S3 target from Open Humans.
    upload_url = '{}?access_token={}'.format(
        OH_DIRECT_UPLOAD, oh_member.get_access_token(**client_info))
    req1 = requests.post(
        upload_url,
        data={'project_member_id': oh_member.oh_id,
              'filename': filehandle.name,
              'metadata': json.dumps(metadata)})
    if req1.status_code != 201:
        raise HTTPError(upload_url, req1.status_code,
                        'Bad response when starting file upload.')

    # Upload to S3 target.
    req2 = requests.put(url=req1.json()['url'], data=filehandle)
    if req2.status_code != 200:
        raise HTTPError(req1.json()['url'], req2.status_code,
                        'Bad response when uploading to target.')

    # Report completed upload to Open Humans.
    complete_url = ('{}?access_token={}'.format(
        OH_DIRECT_UPLOAD_COMPLETE, oh_member.get_access_token(**client_info)))
    req3 = requests.post(
        complete_url,
        data={'project_member_id': oh_member.oh_id,
              'file_id': req1.json()['id']})
    if req3.status_code != 200:
        raise HTTPError(complete_url, req2.status_code,
                        'Bad response when completing upload.')


def index(request):
    """
    Starting page for app.
    """
    proj_config = ProjectConfiguration.objects.get(id=1)
    if proj_config.oh_client_id:
        auth_url = ohapi.api.oauth2_auth_url(
            client_id=proj_config.oh_client_id,
            redirect_uri=OH_OAUTH2_REDIRECT_URI)
    else:
        auth_url = 'http://www.example.com'
    if not proj_config.file_description or not proj_config.oh_client_secret or not proj_config.file_tags or not proj_config.oh_client_id:
        if request.user.is_authenticated and request.user.username == 'admin':
            messages.info(request, "Please set up the app.")
        else:
            messages.info(request, "Please login to set up the app.")
    context = {'auth_url': auth_url,
               'index_page': "".join(proj_config.homepage_text)}
    if request.user.is_authenticated and request.user.username != 'admin':
        return redirect('overview')
    return render(request, 'main/index.html', context=context)


def overview(request):
    client_info = ProjectConfiguration.objects.get(id=1).client_info
    if request.user.is_authenticated and request.user.username != 'admin':
        oh_member = request.user.openhumansmember
        proj_config = ProjectConfiguration.objects.get(id=1)
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   'access_token': oh_member.get_access_token(**client_info),
                   "overview": "".join(proj_config.overview)}
        return render(request, 'main/overview.html', context=context)
    return redirect('index')


def complete(request):
    """
    Receive user from Open Humans. Store data, start data upload task.
    """
    logger.debug("Received user returning from Open Humans.")

    form = None
    proj_config = ProjectConfiguration.objects.get(id=1)

    if request.method == 'GET':
        # Exchange code for token.
        # This creates an OpenHumansMember and associated User account.
        code = request.GET.get('code', '')
        oh_member = oh_code_to_member(code=code)
        if oh_member:
            # Log in the user.
            user = oh_member.user
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
        elif not request.user.is_authenticated:
            logger.debug('Invalid code exchange. User returned to start page.')
            return redirect('/')
        else:
            oh_member = request.user.openhumansmember

        form = UploadFileForm()
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   'form': form,
                   'upload_description': proj_config.upload_description}
        return render(request, 'main/complete.html',
                      context=context)

    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            metadata = {'tags': json.loads(proj_config.file_tags),
                        'description': proj_config.file_description}
            upload_file_to_oh(
                request.user.openhumansmember,
                request.FILES['file'],
                metadata)
        else:
            logger.debug('INVALID FORM')
        return redirect('index')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')


def upload_old(request):
    proj_config = ProjectConfiguration.objects.get(id=1)

    if request.user.is_authenticated:
        context = {'upload_description': proj_config.upload_description}
        return render(request, 'main/upload_old.html',
                      context=context)
    return redirect('index')


def about(request):
    proj_config = ProjectConfiguration.objects.get(id=1)
    context = {'about': proj_config.about,
               'faq': proj_config.faq}
    return render(request, 'main/about.html',
                  context=context)


def list_files(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        oh_member = request.user.openhumansmember
        data = ohapi.api.exchange_oauth2_member(oh_member.get_access_token())
        context = {'files': data['data']}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')
