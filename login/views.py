from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views.generic import ListView

from .forms import CustomAuthenticationForm, RegisterForm, UserEditForm, ProfileEditForm
from login.models import Profile, User

from blog.models import Post


class LoginView(LoginView):
    template_name = "login/login.html"
    form_class = CustomAuthenticationForm


class RegistrationView(FormView):
    template_name = "login/registration.html"
    form_class = RegisterForm

    def form_valid(self, form):
        new_user = form.save()
        profile_username = form.cleaned_data.get("username")
        user = User.objects.get(username=profile_username)
        user.first_name = form.cleaned_data.get("profile_first_name")
        user.last_name = form.cleaned_data.get("profile_last_name")

        user.save()
        Profile.objects.create(
            profile_username=new_user,
            profile_description=form.cleaned_data.get("profile_description"),
        )

        login(self.request, user)
        return redirect("/")


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user, data=request.POST)
        if request.FILES.get("profile_photo"):
            request.user.profile.profile_photo = request.FILES["profile_photo"]
            request.user.profile.save()
        if user_form.is_valid() and profile_form.is_valid():
            request.user.profile.profile_description = request.POST[
                "profile_description"
            ]
            request.user.profile.save()
            profile_form.save()
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "login/edit.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )


class FavoriteView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = self.get_object(id)
        if post.post_user_favorite.filter(id=self.request.user.id).exists():
            post.post_user_favorite.remove(self.request.user)
        else:
            print(post.post_user_favorite.add(request.user))
        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

    def get_object(self, id):
        return get_object_or_404(Post, id=id)


class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = "login/favorites-list.html"

    def get_queryset(self):
        return Post.post_objects.filter(post_user_favorite=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteListView, self).get_context_data(**kwargs)
        context["posts"] = self.get_queryset()
        return context
