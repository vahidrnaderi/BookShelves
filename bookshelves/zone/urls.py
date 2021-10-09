"""Zone URLs."""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import ZoneView

router = routers.DefaultRouter()
router.register("", ZoneView, basename="zones")

urlpatterns = [path("", include(router.urls))]
