from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


class Profile(AbstractBaseUser):
    profile_username = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_description = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(default="img/standart_avatar.png")

    USERNAME_FIELD = "profile_username"

    def __str__(self):
        return f"Профиль пользователя {self.profile_username}"
