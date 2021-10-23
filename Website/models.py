from django.contrib.auth.models import User
from django.db import models


class Class(models.Model):
    digit = models.DecimalField(max_digits=3, decimal_places=0)
    letter = models.CharField(max_length=2)


class Subject(models.Model):
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name='student')
    s_class = models.ForeignKey(to=Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name='teacher')
    subjects = models.ManyToManyField(to=Subject)

    def __str__(self):
        return self.user.username


class Invitation(models.Model):
    code = models.CharField(blank=False, max_length=20)
    invitor = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                related_name='invitor')
    activated = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             null=True,
                             related_name='user')
    type = models.CharField(max_length=100, default="Student")
