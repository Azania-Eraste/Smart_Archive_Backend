# inscriptions/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InscriptionViewSet

router = DefaultRouter()
router.register(r"demandes", InscriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
