# comptes/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Utilisateur


class UtilisateurCreationForm(UserCreationForm):
    # CORRECTION : On déclare explicitement les champs mot de passe pour que l'Admin les trouve
    password_1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Le mot de passe doit contenir au moins 8 caractères.",
    )
    password_2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Entrez le même mot de passe qu'au-dessus pour le vérifier.",
    )

    class Meta:
        model = Utilisateur
        fields = ("email", "nom", "prenom", "role")


class UtilisateurChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ("email", "nom", "prenom", "role", "is_active", "is_staff")
