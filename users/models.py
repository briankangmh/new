from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from . import appenums
from decimal import Decimal


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format('1', filename)

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default=False, upload_to=user_directory_path)
    ugroup = models.CharField(max_length=2)
    country = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, blank=True)
    classg = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=2, default='1')
    ws_status = models.CharField(max_length=2, default='0')
    wallet_balance = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.0'))
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=Decimal('5.0'))
    channel_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    data_updated = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('created', 'CREATED'),
    ('open', 'OPEN'),
    ('pending', 'PENDING'),
    ('resolved', 'RESOLVED'),
    ('closed', 'CLOSED'),
)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='created')
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.title


class TimeOnline(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time_mins = models.IntegerField()
    channel_name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.time_mins
