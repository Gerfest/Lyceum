from django.contrib.auth.models import User
from django.db import models

from Website.models import Subject, Student


class Test(models.Model):
    show_result = models.BooleanField(
        default=True,
        verbose_name='Показывать ответы?',
    )
    max_result = models.PositiveIntegerField(
        default=12,
        verbose_name='Максимальная оценка',
    )
    subject = models.ForeignKey(
        to=Subject,
        verbose_name="Предмет",
        on_delete=models.SET_NULL,
        null=True,
    )
    caption = models.CharField(
        max_length=30,
        verbose_name="Назва тесту",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Опис тесту",
    )
    students = models.ManyToManyField(
        to=Student,
        verbose_name="Студенти",
    )
    creator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тест створив"
    )


class Question(models.Model):
    task = models.TextField(max_length=999)
    answers = models.ForeignKey(to=str,
                                on_delete=models.CASCADE,
                                related_name="Ответы",
                                )


class Answer(models.Model):
    pass
