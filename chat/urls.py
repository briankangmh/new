from django.urls import path, include, re_path

from . import views


urlpatterns = [
    path('twilio/video_call', views.video_call, name='video_call'),
    path('twilio/rooms', views.get_current_rooms, name='rooms'),
    path('twilio/token/<str:room_name>',
         views.generate_token, name='generate_token'),
    path('twilio/chat/token/<str:device>', views.chat_token, name='chat_token'),
]
