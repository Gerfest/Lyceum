# Generated by Django 3.2.8 on 2021-10-29 21:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0009_auto_20211030_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='Вчитель',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Клас',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Опис',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Посилання',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Предмет',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Час кінця',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='Час початку',
        ),
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, max_length=5000, verbose_name='Опис'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='link',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Посилання'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='s_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.class', verbose_name='Клас'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.subject', verbose_name='Предмет'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Website.teacher', verbose_name='Вчитель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_end',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Час кінця'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Час початку'),
            preserve_default=False,
        ),
    ]
