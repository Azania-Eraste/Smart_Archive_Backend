# inscriptions/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Inscription
from .serializers import InscriptionSerializer


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Filtres puissants pour le Dashboard de l'Éducateur/Secrétaire
    # Ex: /api/inscriptions/?statut=EN_ATTENTE&classe=2
    filterset_fields = ["statut", "classe", "annee_scolaire", "eleve"]

    # Tri par date (les plus récentes en premier par défaut)
    ordering_fields = ["date_demande", "statut"]
    ordering = ["-date_demande"]

    def perform_update(self, serializer):
        # Si on met à jour l'inscription, on met à jour "traitee_par"
        # avec l'utilisateur qui fait la modif (ex: l'éducateur qui valide)
        serializer.save(traitee_par=self.request.user)
