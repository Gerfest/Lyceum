# Generated by Django 3.2.8 on 2021-10-31 15:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0017_auto_20211031_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_end',
            field=models.TimeField(default=datetime.datetime(2021, 10, 31, 16, 17, 42, 457795, tzinfo=utc), verbose_name='Час кінця'),
        ),
    ]
