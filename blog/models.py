from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    post_barcode = models.IntegerField(unique=True, default=0)
    post_title = models.CharField(max_length=250)
    post_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post_short_description = models.CharField(
        max_length=250, verbose_name="Краткое описание", default="Краткое описание"
    )
    post_text = models.TextField(verbose_name="Полное описание")
    post_created = models.DateTimeField(auto_now_add=True)
    post_updated = models.DateTimeField(auto_now=True)
    post_slug = models.SlugField()
    post_objects = models.Manager()
    post_rating = models.IntegerField(default=0)
    post_count_view = models.IntegerField(default=0)
    post_user_like = models.ManyToManyField(
        User, related_name="post_liked", default=None, blank=True
    )
    post_user_dislike = models.ManyToManyField(
        User, related_name="post_disliked", default=None, blank=True
    )
    post_user_favorite = models.ManyToManyField(
        User, related_name="favorite", default=None, blank=True
    )

    class Meta:
        ordering = ["-post_created"]

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("blog:post_detail_view", args=[self.post_slug])


class Images(models.Model):
    image = models.FileField(upload_to="static/img/", blank=True, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images", blank=True, null=True
    )
    objects = models.Manager()
