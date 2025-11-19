# etablissement/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import AnneeScolaire, Classe, Matiere, Niveau
from .serializers import (
    AnneeScolaireSerializer,
    ClasseSerializer,
    MatiereSerializer,
    NiveauSerializer,
)


class AnneeScolaireViewSet(viewsets.ModelViewSet):
    queryset = AnneeScolaire.objects.all()
    serializer_class = AnneeScolaireSerializer
    # Tout le monde peut lire, mais il faut être authentifié pour modifier
    permission_classes = [IsAuthenticatedOrReadOnly]


class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
