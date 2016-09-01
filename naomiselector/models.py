from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Game(models.Model):
    hash = models.CharField(max_length=32)
    video = models.CharField(max_length=11)
