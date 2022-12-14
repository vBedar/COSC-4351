# Generated by Django 2.2.27 on 2022-11-07 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Phone', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=100)),
                ('Time', models.DateTimeField()),
                ('GuestNum', models.PositiveIntegerField()),
                ('HoldFee', models.DecimalField(decimal_places=2, max_digits=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Capacity', models.PositiveIntegerField(default=2)),
                ('isReserved', models.BooleanField(default=False)),
            ],
        ),
    ]
