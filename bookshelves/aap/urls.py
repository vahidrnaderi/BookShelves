"""URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.urls import path, include

urlpatterns = [
    path("zone/", include("zone.urls"), name="zone"),
    path("currency/", include("currency.urls"), name="currency"),
    path("blog/", include("blog.urls"), name="blog"),
]
