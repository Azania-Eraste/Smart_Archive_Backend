# dossiers/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DocumentViewSet, EleveViewSet

router = DefaultRouter()
router.register(r"eleves", EleveViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
