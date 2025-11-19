# dossiers/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Document, Eleve
from .serializers import DocumentSerializer, EleveSerializer


class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer
    permission_classes = [IsAuthenticated]

    # --- FILTRES ET RECHERCHE ---
    # Indispensable pour la barre de recherche du frontend
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtres exacts (ex: ?classe=1&statut=ACTIF)
    filterset_fields = ["classe", "statut", "annee_scolaire"]

    # Recherche texte (ex: ?search=Kouadio)
    search_fields = ["nom", "prenom", "matricule"]

    # Tri (ex: ?ordering=nom)
    ordering_fields = ["nom", "date_naissance"]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    # --- CONFIGURATION UPLOAD ---
    # Ces parsers permettent de gérer les requêtes "multipart/form-data"
    # (c'est le format standard pour envoyer des fichiers)
    parser_classes = (MultiPartParser, FormParser)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["eleve", "type_document"]

    def perform_create(self, serializer):
        # Vous pouvez ajouter de la logique ici avant de sauvegarder
        # Par exemple, vérifier que l'utilisateur a le droit d'ajouter ce document
        serializer.save()
