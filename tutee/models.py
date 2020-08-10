from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format('1', filename)

# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user")
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    remarks = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    status = models.CharField(max_length=2)
    view_status = models.CharField(max_length=2, default='0')
    attachment = models.FileField(default=False, upload_to='questions/')
    accepted_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="accepted_by")
    question_type = models.CharField(max_length=2, default='0')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.title


class ViewAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    qid = models.CharField(max_length=100)
    qtitle = models.CharField(max_length=100)
    view_status = models.CharField(max_length=2)
    view_mode = models.CharField(max_length=2)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
