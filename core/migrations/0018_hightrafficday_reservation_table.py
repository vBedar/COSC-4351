# Generated by Django 4.1.1 on 2022-11-23 22:42

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_reservation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='HighTrafficDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(validators=[core.models.date_validator])),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='Table',
            field=models.ForeignKey(default=1, limit_choices_to={'isReserved': False}, on_delete=django.db.models.deletion.CASCADE, to='core.table'),
            preserve_default=False,
        ),
    ]