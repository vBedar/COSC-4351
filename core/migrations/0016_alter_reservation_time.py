# Generated by Django 4.1.1 on 2022-11-19 20:49

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_profile_pphone_alter_reservation_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 19, 20, 49, 18, 396800, tzinfo=datetime.timezone.utc), validators=[core.models.date_validator]),
        ),
    ]
