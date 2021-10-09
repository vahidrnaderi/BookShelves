"""Blog URLs."""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import PostView, TagView, StarView, BookmarkView

router = routers.DefaultRouter()
router.register("posts", PostView, basename="posts")
router.register("tags", TagView, basename="tags")
router.register("stars", StarView, basename="stars")
router.register("bookmarks", BookmarkView, basename="bookmarks")

urlpatterns = [path("", include(router.urls))]
