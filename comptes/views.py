# Create your views here.
# comptes/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .serializers import UtilisateurSerializer

Utilisateur = get_user_model()


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Il faut être connecté pour voir les utilisateurs

    # Endpoint spécial pour récupérer SON propre profil : /api/v1/comptes/users/me/
    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
