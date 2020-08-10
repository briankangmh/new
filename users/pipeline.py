from requests import request, HTTPError
import urllib.request
from django.core.files.base import ContentFile
from users.models import UserProfileInfo


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture" % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['picture']
    if url:
        up, created = UserProfileInfo.objects.get_or_create(user_id=user.id)
        up.photo = url
        up.save()
