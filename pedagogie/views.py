from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
# pedagogie/views.py
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Bulletin, Evaluation, Note
from .serializers import BulletinSerializer, EvaluationSerializer, NoteSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # Permet de filtrer par cours (enseignement), date, etc.
    filterset_fields = ["enseignement", "date"]
    ordering_fields = ["date"]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    # CRUCIAL : Permet au frontend de récupérer toutes les notes d'une évaluation spécifique
    # URL : /api/pedagogie/notes/?evaluation=12
    filterset_fields = ["evaluation", "eleve"]


class BulletinViewSet(viewsets.ModelViewSet):
    queryset = Bulletin.objects.all()
    serializer_class = BulletinSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    # Pour qu'un élève/parent puisse trouver SON bulletin
    filterset_fields = ["eleve", "trimestre", "annee_scolaire"]
