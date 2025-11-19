# pedagogie/serializers.py
from rest_framework import serializers

from .models import Bulletin, Evaluation, Note


class EvaluationSerializer(serializers.ModelSerializer):
    # Pour afficher clairement le nom de la matière et de la classe
    matiere_nom = serializers.CharField(
        source="enseignement.matiere.nom", read_only=True
    )
    classe_nom = serializers.CharField(
        source="enseignement.classe.nom", read_only=True
    )  # Correction: ajout du .nom pour la classe

    class Meta:
        model = Evaluation
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    # Pour afficher le nom de l'élève au lieu de juste son ID
    eleve_nom = serializers.CharField(source="eleve.nom", read_only=True)
    eleve_prenom = serializers.CharField(source="eleve.prenom", read_only=True)

    class Meta:
        model = Note
        fields = "__all__"


class BulletinSerializer(serializers.ModelSerializer):
    eleve_nom = serializers.CharField(source="eleve.nom", read_only=True)

    class Meta:
        model = Bulletin
        fields = "__all__"
