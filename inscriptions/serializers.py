# inscriptions/serializers.py
from rest_framework import serializers

from dossiers.serializers import DocumentSerializer

from .models import Inscription


class InscriptionSerializer(serializers.ModelSerializer):
    # Pour afficher les infos de l'élève et de la classe clairement
    eleve_nom = serializers.CharField(source="eleve.nom", read_only=True)
    eleve_prenom = serializers.CharField(source="eleve.prenom", read_only=True)
    classe_nom = serializers.CharField(source="classe.nom", read_only=True)
    niveau_nom = serializers.CharField(source="classe.niveau.nom", read_only=True)

    # Pour afficher le libellé de l'année (ex: "2024-2025") au lieu de l'ID
    annee_libelle = serializers.CharField(
        source="annee_scolaire.libelle", read_only=True
    )

    # Pour voir le détail des documents fournis (nested)
    documents_details = DocumentSerializer(
        source="documents_fournis", many=True, read_only=True
    )

    class Meta:
        model = Inscription
        fields = "__all__"
        # On empêche la modification de la date de demande manuellement
        read_only_fields = ["date_demande", "traitee_par"]

    def create(self, validated_data):
        # On assigne automatiquement l'utilisateur connecté comme créateur/traitant
        # si besoin (optionnel, dépend de votre logique métier)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["traitee_par"] = request.user
        return super().create(validated_data)
