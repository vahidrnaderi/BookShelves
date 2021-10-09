"""Blog serializers."""
from rest_framework import serializers

from .models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Currency data serializer."""

    class Meta:
        model = Currency
        exclude = ("is_deleted",)
