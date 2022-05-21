import os.path

from django.test import SimpleTestCase, TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils.text import slugify
from blog.models import Post, User
from blog.forms import CreatePostForm
from django.core.files.uploadedfile import SimpleUploadedFile
from uuslug import slugify

NUMBER_OF_POSTS = 5


class TestViews(TestCase):
    password = "raw_password"
    test_user = "test_user"

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            TestViews.test_user, "test@mail.com", TestViews.password
        )

        for post in range(NUMBER_OF_POSTS):
            Post.post_objects.create(
                post_title=f"Пост №{post}",
                post_text=f"Это текст поста №{post}",
                post_slug=f"{post}",
                post_author=user,
                post_barcode=post + 12345123
            )

    def test_list_view(self):
        response = self.client.get(reverse("post_list_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), NUMBER_OF_POSTS)
        self.assertTemplateUsed(response, "blog/list.html")

    def test_detail_view(self):
        response = self.client.get("/blog/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пост №1")
        self.assertContains(response, "Это текст поста №1")
        self.assertTemplateUsed(response, "blog/detail.html")

    def test_create_view(self):
        self.client.login(username="test_user", password="raw_password")
        response = self.client.get(reverse("post_create_view"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/create.html")
        self.client.logout()

    def test_create_view_redirect(self):
        response = self.client.get(reverse("post_create_view"))
        self.assertRedirects(response, "/login?next=/create/", target_status_code=301)

    def test_fill_create_view_true_condition(self):
        self.client.login(username="test_user", password="raw_password")
        data = {
            "post_title": "Заголовок тестового поста",
            "post_text": "Описание тестового поста",
            "post_barcode": 12345
        }
        form = CreatePostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_fill_create_view_false_condition(self):
        self.client.login(username="test_user", password="raw_password")
        data = {
            "post_title": "Заголовок тестового поста",
        }
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_post_request_add_post_with_login(self):
        self.client.login(username="test_user", password="raw_password")
        data = {
            "post_title": f"Заголовок тестового поста POST-запрос валид",
            "post_text": "Описание тестового поста",
            "post_barcode": 1234
        }
        self.client.post("/create/", data=data)
        self.assertTrue(
            Post.post_objects.filter(
                post_title=f"Заголовок тестового поста POST-запрос валид"
            ).exists()
        )

        self.assertEqual(
            Post.post_objects.filter(
                post_title=f"Заголовок тестового поста POST-запрос валид"
            )[0].post_text,
            data["post_text"],
        )
        self.assertEqual(
            len(
                Post.post_objects.filter(
                    post_title=f"Заголовок тестового поста POST-запрос валид"
                )
            ),
            1,
        )

    def test_post_request_add_post_without_login(self):
        data = {
            "post_title": f"Заголовок тестового поста POST-запрос невалид",
            "post_text": "Описание тестового поста",
        }
        response = self.client.post("/create/", data=data)
        self.assertFalse(
            Post.post_objects.filter(post_title=data["post_title"]).exists()
        )

    def test_upload_file_with_login(self):
        self.client.login(username="test_user", password="raw_password")
        file = SimpleUploadedFile("test_upload.csv", b"Title;Description")
        self.client.post(reverse("blog:post_file_upload"), {"file": file})
        self.assertTrue(Post.post_objects.filter(post_title="Title").exists())
        self.assertEqual(len(Post.post_objects.filter(post_title="Title")), 1)
        self.assertEqual(
            Post.post_objects.get(post_title="Title").post_text, "Description"
        )
        self.assertEqual(Post.post_objects.get(post_title="Title").post_slug, "title")
