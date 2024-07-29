from backend.interfaces.auth_token import views as auth_views
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path("token", views.obtain_auth_token, name="token"),
    path("logout", auth_views.logout, name="logout"),
]
