"""Blog serializers."""
from rest_framework import serializers

from .models import Post, Tag, Star, Bookmark


class PostSerializer(serializers.ModelSerializer):
    """Post data serializer."""

    class Meta:
        model = Post
        exclude = ("is_deleted",)


class TagSerializer(serializers.ModelSerializer):
    """Tag data serializer."""

    class Meta:
        model = Tag
        exclude = ("is_deleted",)


class StarSerializer(serializers.ModelSerializer):
    """Star data serializer."""

    class Meta:
        model = Star
        exclude = ("is_deleted",)


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark data serializer."""

    class Meta:
        model = Bookmark
        exclude = ("is_deleted",)
