# Generated by Django 2.2.10 on 2020-05-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20200526_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='callhistory',
            name='call_type',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
