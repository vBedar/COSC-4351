# Generated by Django 4.1.1 on 2022-11-11 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_reservation_user_alter_reservation_id_alter_table_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
    ]