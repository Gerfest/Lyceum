from django.contrib.auth.models import User
from django.db import models


class Invitation(models.Model):
    code = models.CharField(blank=False, max_length=20)
    invitor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='invitor')
    activated = models.BooleanField(default=False)
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, related_name='student')
