# Generated by Django 2.2.4 on 2019-12-09 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0018_auto_20191209_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='school',
        ),
    ]
