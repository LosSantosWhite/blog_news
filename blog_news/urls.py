"""blog_news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from blog.views import PostListView, post_creat_view, PostUpdateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("blog/", include("blog.urls", namespace="blog")),
                  path("login/", include("login.urls", namespace="login")),
                  path("", PostListView.as_view(), name="post_list_view"),
                  path("create/", post_creat_view, name="post_create_view"),
                  path("update/<slug:post_slug>", PostUpdateView.as_view(), name="post_update_view"),
                  path('<parameter>/', PostListView.as_view(), name='post_list_view_sort'),
                  # path('sort_by_raiting_asc/', PostListView.as_view(), name='post_view_raitnig_asc'),
                  # path('sort_by_raiting_desc/', PostListView.as_view(), name='post_update_view_raitnig_desc'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
