"""Base apps models."""
import uuid

from django.db import models


class Base(models.Model):
    """Base model implementation."""

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, editable=False
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.id} {self.created_at} {self.is_deleted}>"
        )
