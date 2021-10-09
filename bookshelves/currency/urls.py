"""Currency URLs."""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import CurrencyView

router = routers.DefaultRouter()
router.register("", CurrencyView, basename="currencies")

urlpatterns = [path("", include(router.urls))]
