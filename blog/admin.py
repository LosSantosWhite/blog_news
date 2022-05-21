from django.contrib import admin
from blog.models import Post, Images


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["post_title", "post_author", "post_created", "post_updated"]
    list_filter = ["post_created", "post_updated"]
    date_hierarchy = "post_created"
    ordering = ["post_created"]
    prepopulated_fields = {"post_slug": ["post_title"]}


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["image", "post"]
