import datetime

from django.db import models
from django.utils import timezone


class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта"),
    ]

    slug = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug
