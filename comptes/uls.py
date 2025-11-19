# comptes/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UtilisateurViewSet

# Le routeur crée automatiquement les URLs standard (/users/, /users/1/...)
router = DefaultRouter()
router.register(r"users", UtilisateurViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # Les endpoints pour le LOGIN (JWT)
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
