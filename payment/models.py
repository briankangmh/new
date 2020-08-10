from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from . import appenums
from decimal import Decimal


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format('1', filename)
# Create your models here.


class WalletTransactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tx_reason = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in appenums.TxReason])
    qid = models.CharField(max_length=100)
    aid = models.CharField(max_length=100)
    from_user_id = models.CharField(max_length=100)
    to_user_id = models.CharField(max_length=100)
    tx_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in appenums.TxType])
    status = models.CharField(max_length=2)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.aid


class TxCommission(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    percent = models.FloatField()
    txc_type = models.CharField(max_length=100)

    def __str__(self):
        return self.txc_type


class PaymentTransactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pay_mode = models.CharField(max_length=100)
    amount = models.FloatField()
    currency_code = models.CharField(max_length=100)
    txid = models.CharField(max_length=100)
    payer_name = models.CharField(max_length=100)
    payer_id = models.CharField(max_length=100)
    payer_email = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)


class QuestionPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.FloatField()
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject
