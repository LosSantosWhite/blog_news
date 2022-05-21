from django.urls import path
from blog.views import PostDetailView, UploadPostView, PostUpdateView, PostLikeView

app_name = "blog"

urlpatterns = [
    path("upload-file/", UploadPostView.as_view(), name="post_file_upload"),
    path("like/", PostLikeView.as_view(), name="post_like_view"),
    path("<slug:post_slug>/", PostDetailView.as_view(), name="post_detail_view"),
]
