"""Base apps models."""
import uuid

from django.db import models


class BaseManager(models.Manager):
    """Base model manager."""

    def get_queryset(self):
        """Django built-in method.

        Filter by is_deleted field.
        """
        return super().get_queryset().filter(is_deleted=False)


class AbstractBase(models.Model):
    """Abstract base model implementation."""

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.created_at}>"


class Base(AbstractBase):
    """Base model implementation."""

    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def delete(self, *args, **kwargs):
        """Django built-in method."""
        self.is_deleted = True
        self.save()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.id} {self.created_at} {self.is_deleted}>"
        )
