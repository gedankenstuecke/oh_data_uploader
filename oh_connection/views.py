import json
import logging
try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError

from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
import requests

from project_admin.models import ProjectConfiguration

from .models import OpenHumansMember
from .forms import UploadFileForm
logger = logging.getLogger(__name__)

OH_BASE_URL = settings.OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DELETE_FILES = OH_API_BASE + '/project/files/delete/'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'

APP_BASE_URL = settings.APP_BASE_URL


def oh_get_member_data(token):
    """
    Exchange OAuth2 token for member data.
    """
    req = requests.get(
        '{}/api/direct-sharing/project/exchange-member/'.format(OH_BASE_URL),
        params={'access_token': token})
    if req.status_code == 200:
        return req.json()
    raise Exception('Status code {}'.format(req.status_code))
    return None


def oh_code_to_member(code):
    """
    Exchange code for token, use this to create and return OpenHumansMember.
    If a matching OpenHumansMember already exists in db, update and return it.
    """
    proj_config = ProjectConfiguration.objects.get(id=1)
    if proj_config.oh_client_secret and proj_config.oh_client_id and code:
        print('{}/complete'.format(APP_BASE_URL))
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': '{}/complete'.format(APP_BASE_URL),
            'code': code,
        }
        req = requests.post(
            '{}/oauth2/token/'.format(OH_BASE_URL),
            data=data,
            auth=requests.auth.HTTPBasicAuth(
                proj_config.oh_client_id,
                proj_config.oh_client_secret
            ))
        data = req.json()
        print("Data: {}".format(str(data)))
        if 'access_token' in data:
            oh_id = oh_get_member_data(
                data['access_token'])['project_member_id']
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
        elif 'error' in req.json():
            logger.debug('Error in token exchange: {}'.format(req.json()))
        else:
            logger.warning('Neither token nor error info in OH response!')
    else:
        logger.error('OH_CLIENT_SECRET or code are unavailable')
    return None


def delete_all_oh_files(oh_member):
    """
    Delete all current project files in Open Humans for this project member.
    """
    requests.post(
        OH_DELETE_FILES,
        params={'access_token': oh_member.get_access_token()},
        data={'project_member_id': oh_member.oh_id,
              'all_files': True})


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
    delete_all_oh_files(oh_member)

    # Get the S3 target from Open Humans.
    upload_url = '{}?access_token={}'.format(
        OH_DIRECT_UPLOAD, oh_member.get_access_token())
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
        OH_DIRECT_UPLOAD_COMPLETE, oh_member.get_access_token()))
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
    context = {'client_id': proj_config.oh_client_id,
               'redirect_uri': '{}/complete'.format(APP_BASE_URL),
               'index_page': "".join(proj_config.homepage_text)}
    if request.user.is_authenticated and request.user.username != 'admin':
        return redirect('overview')
    return render(request, 'oh_connection/index.html', context=context)


def overview(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        oh_member = request.user.openhumansmember
        proj_config = ProjectConfiguration.objects.get(id=1)
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   "overview": "".join(proj_config.overview)}
        return render(request, 'oh_connection/overview.html', context=context)
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
        print("CODE {}".format(code))
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
        return render(request, 'oh_connection/complete.html',
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
        return render(request, 'oh_connection/upload_old.html',
                      context=context)
    return redirect('index')


def about(request):
    proj_config = ProjectConfiguration.objects.get(id=1)
    context = {'about': proj_config.about,
               'faq': proj_config.faq}
    return render(request, 'oh_connection/about.html',
                  context=context)
