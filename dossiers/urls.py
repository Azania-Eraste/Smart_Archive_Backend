# dossiers/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardStatsView, DocumentViewSet, EleveViewSet

router = DefaultRouter()
router.register(r"eleves", EleveViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # Route personnalisée pour les statistiques du dashboard
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
]
