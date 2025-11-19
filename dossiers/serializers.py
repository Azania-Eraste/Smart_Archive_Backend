# dossiers/serializers.py
from rest_framework import serializers

from .models import Document, Eleve


class DocumentSerializer(serializers.ModelSerializer):
    # On ajoute un champ en lecture seule pour voir la taille ou l'URL complète si besoin
    url_fichier = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    def get_url_fichier(self, obj):
        request = self.context.get("request")
        if obj.fichier and request:
            return request.build_absolute_uri(obj.fichier.url)
        return None


class EleveSerializer(serializers.ModelSerializer):
    # Pour afficher le nom de la classe au lieu de juste l'ID
    classe_nom = serializers.CharField(source="classe.nom", read_only=True)
    niveau_nom = serializers.CharField(source="classe.niveau.nom", read_only=True)

    # Pour afficher les documents liés à cet élève (nested serializer)
    # read_only=True car on n'upload pas les documents *dans* l'objet élève,
    # on les crée séparément.
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Eleve
        fields = "__all__"
        # fields inclura: id, matricule, nom, prenom, date_naissance,
        # statut, classe (id), classe_nom, niveau_nom, parents, documents
