from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    TODO Третий вариант создания пользователя в DJANGO

    """
    FEMALE = 'F'
    MALE = 'M'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    HR = 'hr'
    EMPLOYEE = 'employee'
    UNKNOWN = 'unknown'
    ROLE = [(HR, 'hr'), (EMPLOYEE, 'employee'), (UNKNOWN, 'unknown')]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(max_length=8, choices=ROLE, default=UNKNOWN)
