from django.contrib.auth.models import User
from django.db import models


class Profile(User):
    """
    TODO второй вариант создания пользователя в DJANGO

    """
    FEMALE = 'F'
    MALE = 'M'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
