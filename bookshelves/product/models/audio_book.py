"""Audio book product models."""
from base.models import Base
from django.db import models

from .product import Product


class Publisher(Base):
    """Publisher model."""

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class BookAuthor(models.Model):
    """Book author model."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BookSpeaker(models.Model):
    """Book speaker model."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AudioType(models.Model):
    """Audio type model."""

    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class CompatibleDevice(models.Model):
    """Compatible device model."""

    name = models.CharField(max_length=3, unique=True)
    version = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.version}"


class AudioIndex(Base):
    """Audio index model."""

    title = models.CharField(max_length=1024)
    file = models.URLField()
    duration = models.PositiveIntegerField()
    is_downloadable = models.BooleanField(default=False)

    def __str__(self):
        if self.is_deleted:
            return f"{self.title} [deleted]"
        return self.title


class AudioBook(Product):
    """Audio book product model."""

    intro = models.URLField()
    authors = models.ManyToManyField(BookAuthor)
    speakers = models.ManyToManyField(BookSpeaker)
    book_publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="book_publisher"
    )
    audio_publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="audio_publisher"
    )
    indices = models.ForeignKey(AudioIndex, on_delete=models.DO_NOTHING)
    published_year = models.PositiveSmallIntegerField()
    audio_type = models.ForeignKey(AudioType, on_delete=models.DO_NOTHING)
    compatible_devices = models.ManyToManyField(CompatibleDevice)
    is_downloadable = models.BooleanField(default=False)
