import datetime

from django.db import models
from django.utils import timezone

from authentication.models import User  # Третий вариант создания пользователя в DJANGO


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill)

    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['id']

    def __str__(self):
        return self.slug

    @property
    def username(self):
        return self.user.username if self.user else None
