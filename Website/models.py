from django.contrib.auth.models import User
from django.db import models


class Class(models.Model):
    """Model for school classes like 9-A, 10-B, 11-A etc."""
    digit = models.DecimalField(max_digits=3, decimal_places=0)
    letter = models.CharField(max_length=2)


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
