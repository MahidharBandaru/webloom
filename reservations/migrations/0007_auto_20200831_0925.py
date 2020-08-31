# Generated by Django 3.1 on 2020-08-31 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]