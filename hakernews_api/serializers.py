from rest_framework import serializers
from .models import Item, Comment
import uuid


class ReadStorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "author",
            "descendants",
            "score",
            "type",
            "title",
            "url",
            "created_at",
        ]


class ReadCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "parent", "text"]


class ReadAStorySerializer(serializers.ModelSerializer):
    comments = ReadCommentSerializer(many=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "author",
            "descendants",
            "score",
            "type",
            "title",
            "url",
            "created_at",
            "comments",
        ]
