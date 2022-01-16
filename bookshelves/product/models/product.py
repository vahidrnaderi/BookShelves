"""Product models."""
from django.db import models
from base.models import Base
from polymorphic.models import PolymorphicModel
from django.conf import settings


class Tag(Base):
    """Tag model implementation."""

    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class Category(Base):
    """Category model implementation."""

    name = models.CharField(max_length=75)
    parent = models.ForeignKey(
        "self",
        null=True,
        related_name="category_parent",
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


def get_deleted_category():
    """Retrieve or create a category with DELETED_PRODUCT_CATEGORY_NAME."""
    return Category.objects.get_or_create(name=settings.DELETED_PRODUCT_CATEGORY_NAME)


class Product(PolymorphicModel, Base):
    """Product model."""

    name = models.CharField(max_length=120)
    description = models.TextField()
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_deleted_category),
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="product_bookmarks"
    )
    image = models.URLField()
    extra = models.JSONField()

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name
