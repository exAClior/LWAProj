# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class MatchResult(models.Model):
    """
    """
    user_id = models.BigIntegerField(null=False)
    user_name = models.CharField(max_length=300, null=False)
