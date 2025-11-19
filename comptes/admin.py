# comptes/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    # Les colonnes affichées dans la liste
    list_display = ("email", "nom", "prenom", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    # Configuration pour que l'email soit utilisé comme identifiant
    ordering = ("email",)
    search_fields = ("email", "nom", "prenom")

    # Configuration du formulaire d'édition (car on n'a pas de champ 'username')
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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "confirm_password",
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
