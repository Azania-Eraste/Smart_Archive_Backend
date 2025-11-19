# comptes/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (  # Si Eleve est dans comptes, sinon ajustez
    Educateur,
    Parent,
    Professeur,
)

Utilisateur = get_user_model()


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["id", "email", "nom", "prenom", "role", "is_active"]
        # On ne renvoie jamais le mot de passe en lecture
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Surcharge pour hacher le mot de passe correctement lors de la création
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# Serializer spécifique pour le profil Professeur (exemple)
class ProfesseurSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)

    class Meta:
        model = Professeur
        fields = ["utilisateur", "matricule"]
