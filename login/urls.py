from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from login.views import LoginView, LogoutView, RegistrationView, edit, FavoriteView, FavoriteListView

app_name = "login"

urlpatterns = [
    path("", LoginView.as_view(), name="login_view"),
    path("logout/", LogoutView.as_view(), name="logout_view"),
    path("registration/", RegistrationView.as_view(), name="registration_view"),
    path("edit/", edit, name="edit_view"),
    path("favorites/<int:id>", FavoriteView.as_view(), name='favorites_add'),
    path("favorites-list/", FavoriteListView.as_view(), name="favorites_list_view")
]
