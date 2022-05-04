from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    """
    TODO первый вариант создания пользователя в DJANGO

    """
    FEMALE = 'F'
    MALE = 'M'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    user = models.OneToOneField(User, on_delete=CASCADE)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
