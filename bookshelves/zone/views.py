"""Zone views."""
from rest_framework import viewsets

from .models import Zone
from .serializers import ZoneSerializer


class ZoneView(viewsets.ModelViewSet):
    """Zone view set."""

    queryset = Zone.objects.filter(is_deleted=False).all()
    serializer_class = ZoneSerializer
