from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from login.models import Profile, User


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    profile_first_name = forms.CharField(required=False)
    profile_last_name = forms.CharField(required=False)
    profile_description = forms.Textarea()
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_description", "profile_photo"]
