# Generated by Django 3.1.1 on 2020-09-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='channel',
            field=models.CharField(default='-', max_length=100),
            preserve_default=False,
        ),
    ]
