# Generated by Django 2.2.10 on 2020-05-27 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_mode', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('currency_code', models.CharField(max_length=100)),
                ('txid', models.CharField(max_length=100)),
                ('payer_name', models.CharField(max_length=100)),
                ('payer_id', models.CharField(max_length=100)),
                ('payer_email', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField()),
                ('update_time', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
