"""Zone app models."""
from django.db import models

from base.models import Base
from currency.models import Currency


class Zone(Base):
    """Zone model implementation."""

    name = models.CharField(max_length=25, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    currency = models.ForeignKey(
        Currency, null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f"{self.name}({self.abbreviation})"


class Language(Base):
    """Language model implementation."""

    name = models.CharField(max_length=25, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name}({self.abbreviation})"
