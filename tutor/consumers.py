from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import asyncio

# python
import json
from datetime import date
import datetime

# django
from django.utils import timezone
from django.db.models import F

# models
from users.models import UserProfileInfo, TimeOnline


class NoseyConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def update_user_status(self, user, ws_status, channel_name):
        """
        Updates the user `status.
        `status` can be one of the following status: 'online', 'offline' or 'away'
        """
        # print("--------------------->","update_user_status")
        now = timezone.now()
        return UserProfileInfo.objects.filter(user_id=user).update(ws_status=ws_status, channel_name=channel_name, data_updated=now)

    @database_sync_to_async
    def track_online_time(self, user):
        today = date.today()
        now = timezone.now()
        time_online = TimeOnline.objects.filter(user_id=user.id, date=today)
        if time_online.count() == 0:
            new_today_time = TimeOnline(
                user=user, time_mins=0, channel_name=self.channel_name, date=today, date_updated=now)
            new_today_time.save()
        else:
            time_online.update(
                channel_name=self.channel_name, date_updated=now)

        return time_online

    @database_sync_to_async
    def track_online_close(self, user):
        today = date.today()
        now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
        prev = TimeOnline.objects.get(channel_name=self.channel_name)
        diff = now - prev.date_updated
        print(diff.total_seconds())
        time_mins = int(prev.time_mins) + int(diff.total_seconds())
        time_online = TimeOnline.objects.filter(
            date=today, channel_name=self.channel_name).update(time_mins=time_mins, date_updated=now)

        return time_online

    async def connect(self):
        await self.accept()
        user = self.scope['user']
        await self.channel_layer.group_add("active", self.channel_name)
        # print("---------------->", "self.scope", self.scope)
        await self.update_user_status(user.id, 1, self.channel_name)
        await self.track_online_time(user)
        # print(f"Added {self.channel_name} channel to active")
        print("connect", user.first_name, self.channel_name)

    async def disconnect(self, close_code):
        user = self.scope['user']
        await self.channel_layer.group_discard("active", self.channel_name)
        # print(f"Removed {self.channel_name} channel to active")
        await self.update_user_status(user.id, 0, self.channel_name)
        await self.track_online_close(user)
        print("disconnect", user.first_name, self.channel_name)

    async def user_active(self, event):
        await self.send_json(event)
        # print(f"Got message {event} at {self.channel_name}")
        # await self.channel_layer.send(
        #     event['channel_name'],
        #     {
        #         'type':'send_message',
        #         'user':'nivu',
        #         'message':'Insufficient Amount to Play',
        #         'status':'400'
        #     }
        # )

    async def new_question(self, event):
        # print("------------------------>", "new_question")
        # print(event)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'event': event['event'],
            'title': event['title'],
            'qid': event['qid'],
            'subject': event['subject'],
            'desc': event['desc']
        }))

    async def incoming_call(self, event):
        # print("------------------------>", "incoming_call")
        # print(event)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'event': event['event'],
            'tutee_name': event['tutee_name'],
            'room_name': event['room_name'],
            'subject': event['subject'],
            'tutee_id': event['tutee_id'],
            'call_type': event['call_type']
        }))
