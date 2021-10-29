# Generated by Django 3.2.8 on 2021-10-29 23:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0011_auto_20211030_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_end',
            field=models.TimeField(default=datetime.datetime(2021, 10, 29, 23, 52, 19, 468588, tzinfo=utc), verbose_name='Час кінця'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_start',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Час початку'),
        ),
    ]
