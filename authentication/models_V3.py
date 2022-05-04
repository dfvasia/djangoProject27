from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    TODO Третий вариант создания пользователя в DJANGO

    """
    FEMALE = 'F'
    MALE = 'M'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
