# comptes/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import (  # <-- Importez les formulaires
    UtilisateurChangeForm,
    UtilisateurCreationForm,
)
from .models import (
    Directeur,
    Educateur,
    Fondateur,
    Parent,
    Professeur,
    Secrétaire,
    Utilisateur,
)


# --- Personnalisation de l'affichage de l'Utilisateur ---
class UtilisateurAdmin(BaseUserAdmin):
    # On lie les formulaires personnalisés
    form = UtilisateurChangeForm
    add_form = UtilisateurCreationForm

    # Les colonnes affichées dans la liste
    list_display = ("email", "nom", "prenom", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    ordering = ("email",)
    search_fields = ("email", "nom", "prenom")

    # Formulaire d'édition (quand on modifie un user existant)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations Personnelles", {"fields": ("nom", "prenom", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    # Formulaire d'ajout (C'est ici que ça change !)
    # On utilise 'password_1' et 'password_2' qui sont gérés par le formulaire de création
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password_1",
                    "password_2",
                    "nom",
                    "prenom",
                    "role",
                ),
            },
        ),
    )


# --- Administration des Profils ---


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "telephone")
    search_fields = ("utilisateur__nom", "utilisateur__prenom", "telephone")


@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "matricule")
    search_fields = ("utilisateur__nom", "matricule")


@admin.register(Educateur)
class EducateurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "matricule")


@admin.register(Secrétaire)
class SecretaireAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "matricule", "bureau")


@admin.register(Directeur)
class DirecteurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "matricule")


# Enregistrement du modèle Utilisateur personnalisé
admin.site.register(Utilisateur, UtilisateurAdmin)
# admin.site.register(Fondateur) # Optionnel si besoin
