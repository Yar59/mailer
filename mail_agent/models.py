# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Subscriber(models.Model):
    name = models.CharField(
        'ФИО',
        max_length=50
    )
    email = models.EmailField(
        'e-mail',
        max_length=100,
    )
    birthday = models.DateField(
        'день рождения',
        max_length=50,
    )

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'

    def __str__(self):
        return self.name
