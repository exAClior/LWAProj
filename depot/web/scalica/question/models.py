# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Questions(models.Model):
    """
    """
    question = models.CharField(max_length=300, null=False)


class UserAnswer(models.Model):
    """
    """
    user_id = models.BigIntegerField(null=False)
    question_id = models.BigIntegerField(null=False)
    answer = models.CharField(max_length=300, null=False)


