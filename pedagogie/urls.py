# pedagogie/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BulletinViewSet, EvaluationViewSet, NoteViewSet

router = DefaultRouter()
router.register(r"evaluations", EvaluationViewSet)
router.register(r"notes", NoteViewSet)
router.register(r"bulletins", BulletinViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
