"""Currency views."""
from rest_framework import viewsets

from .models import Currency
from .serializers import CurrencySerializer


class CurrencyView(viewsets.ModelViewSet):
    """Currency view set."""

    queryset = Currency.objects.filter(is_deleted=False).all()
    serializer_class = CurrencySerializer
