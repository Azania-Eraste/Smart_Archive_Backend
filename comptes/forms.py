# comptes/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Utilisateur


class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        # On liste les champs qu'on veut voir à la création
        # Note: Les champs mots de passe sont ajoutés automatiquement par UserCreationForm
        fields = ("email", "nom", "prenom", "role")


class UtilisateurChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ("email", "nom", "prenom", "role", "is_active", "is_staff")
