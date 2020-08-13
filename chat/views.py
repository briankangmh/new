# django
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import F
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# python
from decimal import Decimal
import time
import calendar

# models
from users.models import UserProfileInfo
from chat.models import CallHistory
from . import appenums
from users.models import Subject

# websocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.jwt.client import ClientCapabilityToken

# Create your views here.


def generate_token(request, room_name):
    print("------------->", "generate_token")
    message = "Token Generated"
    status = True
    if request.user.is_authenticated:

        # Substitute your Twilio AccountSid and ApiKey details
        ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
        API_KEY_SID = settings.TWILIO_API_KEY_SID
        API_KEY_SECRET = settings.TWILIO_API_KEY_SECRET

        # Create an Access Token
        token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET)

        # Set the Identity of this token
        token.identity = request.user.id

        # Grant access to Video
        grant = VideoGrant(room=room_name)
        token.add_grant(grant)

        # Serialize the token as a JWT
        jwt = token.to_jwt()
        data = {
            'status': status,
            'msg': message,
            'token': jwt.decode('utf-8')
        }
    return JsonResponse(data)


def create_room(room_name):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    room = client.video.rooms.create(unique_name=room_name)
    return room


def get_room(room_name):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    try:
        call_history = CallHistory.objects.filter(
            room_name=room_name).latest('date_created')
    except ObjectDoesNotExist:
        return "not-available"
    room = client.video.rooms(call_history.sid).fetch()
    return room.status


def video_call(request):
    print("------------->", "video_call")
    channel_layer = get_channel_layer()
    message = "Error Creating Room"
    status = False
    room_name = ""

    if request.user.is_authenticated:
        if request.method == 'POST':
            question_id = request.POST.get('question_id')
            subject = request.POST.get('subject')
            tutor_id = request.POST.get('tutor_id')
            call_type = request.POST.get('call_type')
            print(question_id, subject, tutor_id, call_type)
            room_name = "room_tutee_" + \
                str(request.user.id) + "_tutor_" + str(tutor_id)
            print(room_name)
            if get_room(room_name) == "in-progress":
                print("inp")
                message = "Room Already Active"
                status = True
            else:
                print("new room")
                try:
                    room = create_room(room_name)
                    sid = room.sid
                    date_created = room.date_created
                    date_updated = room.date_updated
                    duration = room.duration
                    call = CallHistory(user=request.user, qid=question_id, subject=subject, tutor_id=tutor_id, room_name=room_name,
                                       sid=sid, call_type=call_type, date_created=date_created, date_updated=date_updated, duration=duration)
                    call.save()
                    message = "Room Created Successfully"
                except Exception as e:
                    print("Room Already Exists", e)
                    message = "Room Already Exists"
                status = True
            tutor = UserProfileInfo.objects.get(user_id=tutor_id)
            async_to_sync(channel_layer.send)(
                tutor.channel_name, {"type": "incoming_call",
                                     "event": "Incoming Call",
                                     "tutee_name": request.user.first_name,
                                     "room_name": room_name,
                                     "call_type": call_type,
                                     "subject": subject,
                                     "tutee_id": request.user.id})

    data = {
        'status': status,
        "msg": message,
        "room_name": room_name
    }
    return JsonResponse(data)


def get_current_rooms(request):
    message = "Rooms"
    status = True
    rooms = ""

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    if request.user.is_authenticated:
        rooms = client.video.rooms.list(limit=20)
        for record in rooms:
            print(record)

    data = {
        'status': status,
        "msg": message,
        "rooms": "rooms"
    }
    return JsonResponse(data)


def get_capability_token(request):
    """Respond to incoming requests."""
    twiml_sid = "AP4488b778ec049eac9a19a8d82c785cd6"

    # Find these values at twilio.com/console
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    capability = ClientCapabilityToken(account_sid, auth_token)

    # Twilio Application Sid
    application_sid = twiml_sid
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming('joey')
    token = capability.to_jwt()

    return JsonResponse(token, mimetype='application/jwt')


def chat_token(request, device):
    if request.user.is_authenticated:

        # print("---------> chat_token", request.COOKIES)
        identity = request.user.username
        ts = calendar.timegm(time.gmtime())

        device_id = request.COOKIES['sessionid']  # unique device ID

        # print('------------------->chat_token', identity, device_id, device)

        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY_SID
        api_secret = settings.TWILIO_API_KEY_SECRET
        chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

        token = AccessToken(account_sid, api_key,
                            api_secret, identity=identity)
        # print("---------> identity", identity)
        # print("---------> token", token)

        # Create a unique endpoint ID for the device
        endpoint = "TitanChatRoom:{0}:{1}".format(identity, device_id)
        # print("endpoint", endpoint)

        if chat_service_sid:
            chat_grant = ChatGrant(endpoint_id=endpoint,
                                   service_sid=chat_service_sid)
            token.add_grant(chat_grant)

        response = {
            'identity': identity,
            'token': token.to_jwt().decode('utf-8')
        }

        return JsonResponse(response)
    else:
        response = {
            'message': "User Not Authenticated",
            'status': False
        }

        return JsonResponse(response)
