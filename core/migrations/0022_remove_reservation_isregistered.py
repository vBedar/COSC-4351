# Generated by Django 4.1.1 on 2022-11-27 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_reservation_isregistered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='isRegistered',
        ),
    ]
