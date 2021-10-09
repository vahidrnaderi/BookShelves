"""Currency app models."""
from django.db import models

from base.models import Base


class Currency(Base):
    """Currency model implementation."""

    name = models.CharField(max_length=30, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    sign = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return f"{self.name}({self.abbreviation})"
