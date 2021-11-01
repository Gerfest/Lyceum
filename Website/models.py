from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Class(models.Model):
    """Model for school classes like 9-A, 10-B, 11-A etc."""
    digit = models.DecimalField(max_digits=3, decimal_places=0)
    letter = models.CharField(max_length=2)

    def __str__(self):
        return str(self.digit) + '-' + self.letter


class Subject(models.Model):
    """Model containing subject in school"""
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class Student(models.Model):
    """Model for a user who is also a student"""
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name='student')
    s_class = models.ForeignKey(to=Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    """Model for a user who is also a teacher"""
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name='teacher')
    subjects = models.ManyToManyField(to=Subject)

    phone = PhoneNumberField(blank=True)

    show_phone = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Invitation(models.Model):
    """Model for storing invitations"""
    code = models.CharField(blank=False, max_length=20)
    invitor = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                related_name='invitor')
    activated = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             null=True,
                             related_name='user')
    type = models.CharField(max_length=100, default="Student")


class Lesson(models.Model):
    """Lesson model that will be displayed in schedule"""
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE,
                                verbose_name="Предмет")
    date = models.DateField(verbose_name="Дата", default=timezone.now)
    time_start = models.TimeField(verbose_name="Час початку",
                                  default=timezone.now)
    time_end = models.TimeField(verbose_name="Час кінця",
                                default=timezone.now()
                                )
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE,
                                verbose_name="Вчитель", null=True)
    s_class = models.ForeignKey(to=Class, on_delete=models.CASCADE,
                                verbose_name="Клас")
    link = models.CharField(max_length=1000, blank=True,
                            verbose_name="Посилання")
    type = models.CharField(verbose_name="Тип",
                            max_length=100,
                            choices=[("lesson", "Урок"), ("test", "Тест")],
                            default="lesson"
                            )
    description = models.TextField(max_length=5000, blank=True,
                                   verbose_name="Опис")

    def __str__(self):
        return f"{self.subject}, {self.s_class}, {self.date} {self.time_start}-{self.time_end}"
