from django.contrib.auth.models import User
from django.db import models


class Invitation(models.Model):
    code = models.CharField(blank=False, max_length=20)
    invitor = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    invited = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
