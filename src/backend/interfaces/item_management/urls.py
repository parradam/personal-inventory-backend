from django.urls import path

from backend.interfaces.item_management import views

urlpatterns = [path("items/", views.ItemList.as_view())]
