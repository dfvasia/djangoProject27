from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from authentication.Serializers import UserCreateSerializer
from authentication.models import User


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
