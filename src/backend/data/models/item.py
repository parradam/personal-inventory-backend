from django.db import models

from .custom_user import CustomUser


class Item(models.Model):
    name = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50, null=True)
    owner = models.CharField(max_length=50, null=True)
    used_from = models.DateTimeField()
    used_to = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
