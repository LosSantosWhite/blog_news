import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView, View
from blog.forms import UploadPostForm, CreateImageForm, CreatePostForm
from django.http import HttpResponseRedirect

from uuslug import slugify

from blog.models import Post, Images


class PostListView(ListView):
    """
    Отображение списка постов
    """

    paginate_by = 5
    model = Post
    context_object_name = "posts"
    template_name = "blog/list.html"

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        context["page"] = self.paginate_by

        if self.kwargs.get("parameter"):
            context["posts"] = self.get_queryset(self.kwargs.get("parameter"))
        return context

    def get(self, request, **kwargs):
        if self.request.GET.get("count_post"):
            self.paginate_by = int(self.request.GET.get("count_post"))
        return super(PostListView, self).get(request, **kwargs)

    def get_queryset(self, parameter="-post_created"):
        return Post.post_objects.order_by(str(parameter))


class PostDetailView(DetailView):
    """
    Детальное отображение постов
    """

    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        object.post_count_view += 1
        object.save()
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Post.post_objects.get(post_slug=self.kwargs["post_slug"])

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        return context


@login_required(login_url="/login")
def post_creat_view(request):
    if request.POST:
        post_form = CreatePostForm(data=request.POST)
        image_form = CreateImageForm(data=request.POST, files=request.FILES)

        if post_form.is_valid() and image_form.is_valid():
            post_form.instance.post_author = request.user
            post_form.instance.post_slug = slugify(
                post_form.cleaned_data.get("post_title")
            )

            image_form.instance.post = post_form.instance
            images = request.FILES.getlist("image")
            post_form.save()
            for image in images:
                _ = Images(image=image, post=post_form.instance).save()

            return redirect("/")
    else:
        post_form = CreatePostForm()
        image_form = CreateImageForm()
    return render(
        request,
        "blog/create.html",
        context={"post_form": post_form, "image_form": image_form},
    )


class UploadPostView(LoginRequiredMixin, FormView):
    """
    Загрузка нескольких блогов через csv файл
    """

    template_name = "blog/upload_file.html"
    form_class = UploadPostForm
    login_url = "/login/"

    def form_valid(self, form):
        file = form.cleaned_data.get("file").read()
        post_text = file.decode("utf-8").split("\n")
        csv_reader = csv.reader(post_text, delimiter=";", quotechar='"')
        for row in csv_reader:
            Post.post_objects.create(
                post_slug=slugify(row[0]),
                post_title=row[0],
                post_author=self.request.user,
                post_text=row[1],
                post_barcode=row[2],
            )
        return super(UploadPostView, self).form_valid(form)

    def get_success_url(self):
        return reverse("post_list_view")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение записи
    """

    model = Post
    template_name = "blog/post_update.html"
    fields = ["post_title", "post_text", "post_slug", "post_short_description"]

    def get_object(self, queryset=None):
        return get_object_or_404(Post, post_slug=self.kwargs.get("post_slug"))

    def form_valid(self, form):
        return super(PostUpdateView, self).form_valid(form)

    def test_func(self):
        """
        Проверка, что пользователь это автор и
        позволяет ему редактировать пост иначе 403
        """
        obj = self.get_object()
        return obj.post_author == self.request.user


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """
        Подсчет 'лайков' и 'дизлайков'
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        post_id = self.request.POST.get("dislike") or self.request.POST.get("like")
        post = Post.post_objects.get(id=post_id)
        if self.request.user in post.post_user_like.filter(username=self.request.user):
            if self.request.POST.get("like"):
                post.post_user_like.remove(self.request.user)
                post.post_rating -= 1
            elif self.request.POST.get("dislike"):
                post.post_user_like.remove(self.request.user)
                post.post_user_dislike.add(self.request.user)
                post.post_rating -= 2
        elif self.request.user in post.post_user_dislike.filter(
            username=self.request.user
        ):
            if self.request.POST.get("dislike"):
                post.post_rating += 1
                post.post_user_dislike.remove(self.request.user)

            elif self.request.POST.get("like"):
                post.post_user_like.add(self.request.user)
                post.post_user_dislike.remove(self.request.user)
                post.post_rating += 2
        else:
            if self.request.POST.get("like"):
                post.post_rating += 1
                post.post_user_like.add(self.request.user)

            else:
                post.post_rating -= 1
                post.post_user_dislike.add(self.request.user)
        post.save()

        return HttpResponseRedirect(
            reverse("blog:post_detail_view", args=[post.post_slug])
        )
