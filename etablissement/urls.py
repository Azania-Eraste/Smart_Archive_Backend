# etablissement/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnneeScolaireViewSet, ClasseViewSet, MatiereViewSet, NiveauViewSet

router = DefaultRouter()
router.register(r"annees", AnneeScolaireViewSet)
router.register(r"niveaux", NiveauViewSet)
router.register(r"classes", ClasseViewSet)
router.register(r"matieres", MatiereViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
