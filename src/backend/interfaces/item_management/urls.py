from django.urls import path

from backend.interfaces.item_management import views

urlpatterns = [path("items/", views.create_item, name="item-create")]
