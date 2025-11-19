# etablissement/serializers.py
from rest_framework import serializers

from .models import AnneeScolaire, Classe, Ecole, Enseignement, Matiere, Niveau


class AnneeScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeScolaire
        fields = "__all__"


class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = "__all__"


class ClasseSerializer(serializers.ModelSerializer):
    # Pour afficher le nom du niveau au lieu de juste l'ID
    niveau_nom = serializers.CharField(source="niveau.nom", read_only=True)

    class Meta:
        model = Classe
        fields = ["id", "ecole", "niveau", "niveau_nom", "nom", "educateur_referent"]


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = "__all__"
