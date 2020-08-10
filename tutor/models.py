from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format('1', filename)

# Create your models here.


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    qid = models.CharField(max_length=100)
    answer = models.TextField(max_length=1000)
    remarks = models.CharField(max_length=100)
    status = models.CharField(max_length=2)
    attachment = models.ImageField(
        default=False, upload_to=user_directory_path)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.answer


class TutorFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    qid = models.CharField(max_length=100)
    aid = models.CharField(max_length=100)
    tutor_id = models.CharField(max_length=100)
    rating = models.IntegerField()
    remarks = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()
