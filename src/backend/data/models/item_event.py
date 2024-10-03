from django.db import models

from backend.data.models.item import Item


class ItemEvent(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="events")
    description = models.CharField(max_length=200)
    event_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.description}"
