"""Blog app models."""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from base.models import Base
from zone.models import Zone, Language


class Tag(Base):
    """Tag model implementation."""

    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class Post(Base):
    """Post model implementation."""

    title = models.CharField(max_length=1024, null=False, unique=True)
    brief = models.TextField(null=False)
    content = models.TextField(null=False)
    tags = models.ManyToManyField(Tag, related_name="tags")
    is_draft = models.BooleanField(default=False)
    previous = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.is_deleted:
            return f"{self.title} [deleted]"
        if self.is_draft:
            return f"{self.title} [draft]"
        if self.previous:
            return f"{self.title} [continue]"
        return self.title


class Star(Base):
    """Star (posts) model implementation."""

    star = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.STAR_MIN_VALUE),
            MaxValueValidator(settings.STAR_MAX_VALUE),
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title}[{self.star}]"


class Bookmark(Base):
    """Bookmark (posts) model implementation."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
