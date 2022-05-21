from django.test import SimpleTestCase, TestCase
from blog.models import Post, User


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        password = "raw_password"
        test_user = "test_user"
        user = User.objects.create_user(test_user, "test@mail.com", password)
        user.save()

        post = Post.post_objects.create(
            post_title="Пост",
            post_text="Это текст поста",
            post_slug="post",
            post_author=user,
        )
        post.save()

    def test_model_str(self):
        post = Post.post_objects.get(post_slug="post")
        self.assertEqual(post.__str__(), "Пост")

    def test_get_abs_url(self):
        post = Post.post_objects.get(post_slug="post")
        self.assertEqual(post.get_absolute_url(), "/blog/post/")
