# Generated by Django 3.2.8 on 2021-10-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0006_auto_20211023_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='type',
            field=models.CharField(default='Student', max_length=100),
        ),
    ]
