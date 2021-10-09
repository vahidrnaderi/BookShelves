"""Blog views."""
from rest_framework import viewsets

from .models import Post, Tag, Star, Bookmark
from .serializers import (
    PostSerializer,
    TagSerializer,
    StarSerializer,
    BookmarkSerializer,
)


class PostView(viewsets.ModelViewSet):
    """Post view set."""

    queryset = Post.objects.filter(is_deleted=False).all()
    serializer_class = PostSerializer


class TagView(viewsets.ModelViewSet):
    """Tag view set."""

    queryset = Tag.objects.filter(is_deleted=False).all()
    serializer_class = TagSerializer


class StarView(viewsets.ModelViewSet):
    """Star view set."""

    queryset = Star.objects.filter(is_deleted=False).all()
    serializer_class = StarSerializer


class BookmarkView(viewsets.ModelViewSet):
    """Bookmark view set."""

    queryset = Bookmark.objects.filter(is_deleted=False).all()
    serializer_class = BookmarkSerializer
