from django.urls import path

from backend.interfaces.item_management import views

urlpatterns = [path("items/", views.ItemList.as_view())]
urlpatterns += [path("items/<int:pk>", views.ItemDetail.as_view())]
