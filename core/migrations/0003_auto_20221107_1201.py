# Generated by Django 2.2.27 on 2022-11-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20221107_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Points',
            field=models.PositiveIntegerField(default=0, max_length=100),
        ),
    ]
