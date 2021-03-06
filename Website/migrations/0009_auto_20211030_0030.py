# Generated by Django 3.2.8 on 2021-10-29 21:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0008_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='description',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='link',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='s_class',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='time_start',
        ),
        migrations.AddField(
            model_name='lesson',
            name='Вчитель',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.teacher'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='Клас',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.class'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='Опис',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AddField(
            model_name='lesson',
            name='Посилання',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='lesson',
            name='Предмет',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='Час кінця',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='Час початку',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
