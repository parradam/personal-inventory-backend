from django.urls import path
from rest_framework.authtoken import views

from backend.interfaces.auth_token import views as auth_views

urlpatterns = [
    path("token", views.obtain_auth_token, name="token"),
    path("check", auth_views.AuthCheckView.as_view(), name="check"),
    path("register", auth_views.RegisterView.as_view(), name="register"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
