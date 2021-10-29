# Generated by Django 3.2.8 on 2021-10-29 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0007_invitation_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('link', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=5000)),
                ('s_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.class')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.teacher')),
            ],
        ),
    ]
