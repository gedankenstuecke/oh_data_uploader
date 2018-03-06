import ohapi
from open_humans.models import OpenHumansMember
import logging

logger = logging.getLogger(__name__)


def get_create_member(data):
    '''
    use the data returned by `ohapi.api.oauth2_token_exchange`
    and return an oh_member object
    '''
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
