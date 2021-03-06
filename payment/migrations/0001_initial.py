# Generated by Django 2.2.10 on 2020-05-26 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_reason', models.CharField(choices=[('ANSW', 'Answer'), ('CHAT', 'Chat'), ('ACHAT', 'Achat'), ('VCHAT', 'Vchat')], max_length=10)),
                ('qid', models.CharField(max_length=100)),
                ('aid', models.CharField(max_length=100)),
                ('from_user_id', models.CharField(max_length=100)),
                ('to_user_id', models.CharField(max_length=100)),
                ('tx_type', models.CharField(choices=[('CR', 'Credit'), ('DB', 'Debit')], max_length=10)),
                ('status', models.CharField(max_length=2)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TxCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField()),
                ('txc_type', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
