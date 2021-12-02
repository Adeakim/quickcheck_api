from django.db import models
import uuid


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    item_id = models.PositiveIntegerField(null=True)
    descendants = models.PositiveIntegerField(null=True)
    score = models.PositiveIntegerField(null=True)
    url = models.URLField(max_length=2000, null=True)
    time = models.PositiveIntegerField(null=True)
    is_hackernews = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["time"]
        verbose_name_plural = "Items"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_id = models.PositiveIntegerField(null=True)
    author = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(null=True)
    time = models.PositiveBigIntegerField(null=True)
    is_hacker_comment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["time"]
        verbose_name_plural = "Comments"
