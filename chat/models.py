from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from . import appenums


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format('1', filename)
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name


class CallHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    qid = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    tutor_id = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    sid = models.CharField(max_length=100)
    call_type = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()
    duration = models.IntegerField()
