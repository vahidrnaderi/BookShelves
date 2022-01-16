"""Product views."""
from .audio_book import (
    AudioBookViewSet,
    AudioIndexViewSet,
    AudioTypeViewSet,
    BookAuthorViewSet,
    BookSpeakerViewSet,
    CompatibleDeviceViewSet,
    PublisherViewSet,
)
from .product import BookmarkViewSet, CategoryViewSet, TagViewSet

__all__ = (
    "AudioTypeViewSet",
    "TagViewSet",
    "CategoryViewSet",
    "PublisherViewSet",
    "BookmarkViewSet",
    "AudioBookViewSet",
    "AudioIndexViewSet",
    "BookAuthorViewSet",
    "BookSpeakerViewSet",
    "CompatibleDeviceViewSet",
)
