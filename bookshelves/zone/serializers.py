"""Blog serializers."""
from rest_framework import serializers

from .models import Zone


class ZoneSerializer(serializers.ModelSerializer):
    """Zone data serializer."""

    class Meta:
        model = Zone
        exclude = ("is_deleted",)
