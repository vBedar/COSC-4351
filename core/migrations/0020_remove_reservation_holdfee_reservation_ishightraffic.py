# Generated by Django 4.1.1 on 2022-11-26 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_reservation_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='HoldFee',
        ),
        migrations.AddField(
            model_name='reservation',
            name='isHighTraffic',
            field=models.BooleanField(default=False),
        ),
    ]
