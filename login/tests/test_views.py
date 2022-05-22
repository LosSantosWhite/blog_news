from django.contrib.auth import authenticate
from django.urls import reverse
from uuslug import slugify

from login.models import Profile, User
from blog.models import Post

from django.test import TestCase, Client


class TestProfileView(TestCase):
    def setUp(self) -> None:
        self.register_data = {
            "username": "new_test_user",
            "password1": "8086935googleHELPme",
            "password2": "8086935googleHELPme",
            "profile_first_name": "Test",
            "profile_last_name": "Update",
        }
        self.register_url = reverse("login:registration_view")

        self.data_to_edit = {
            "first_name": "New First Name",
            "last_name": "New Last Name",
            "profile_description": "New profile description",
        }

    def test_register_user_func_tool(self):
        """
        Проверка регистрации пользователя и изменение и сохранение данных в профиле
        """
        response = self.client.post(self.register_url, data=self.register_data)
        self.assertRedirects(response, "/")

        self.assertEqual(
            User.objects.get(username=self.register_data["username"]).username,
            self.register_data["username"],
        )

        self.client.post(reverse("login:edit_view"), data=self.data_to_edit)
        self.assertEqual(
            User.objects.get(
                username=User.objects.get(username=self.register_data["username"])
            ).first_name,
            self.data_to_edit["first_name"],
        )
        self.assertEqual(
            User.objects.get(username=self.register_data["username"]).first_name,
            self.data_to_edit["first_name"],
        )
        self.assertEqual(
            Profile.objects.get(
                profile_username=User.objects.get(
                    username=self.register_data["username"]
                )
            ).profile_description,
            self.data_to_edit["profile_description"],
        )
