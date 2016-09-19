from __future__ import unicode_literals

from django.db import models


class DataModel(models.Model):
    value = models.IntegerField()
