# Generated by Django 4.1.1 on 2022-11-30 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_remove_reservation_isregistered'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='TableT',
            field=models.ForeignKey(limit_choices_to={'isReserved': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TableT', to='core.table'),
        ),
    ]
