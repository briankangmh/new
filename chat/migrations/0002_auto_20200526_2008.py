# Generated by Django 2.2.10 on 2020-05-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callhistory',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
