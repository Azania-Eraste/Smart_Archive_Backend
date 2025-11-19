# etablissement/admin.py
from django.contrib import admin

from .models import AnneeScolaire, Classe, Ecole, Enseignement, Matiere, Niveau


@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ("libelle", "date_debut", "date_fin", "est_active")
    list_editable = (
        "est_active",
    )  # Permet de cocher la case directement dans la liste


@admin.register(Ecole)
class EcoleAdmin(admin.ModelAdmin):
    list_display = ("nom", "ville", "pays")


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ("nom", "ordre")
    ordering = ("ordre",)


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ("nom", "niveau", "ecole", "educateur_referent")
    list_filter = ("niveau", "ecole")
    search_fields = ("nom",)


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(Enseignement)
class EnseignementAdmin(admin.ModelAdmin):
    list_display = ("professeur", "matiere", "classe", "coefficient")
    list_filter = ("classe", "matiere")
    search_fields = ("professeur__utilisateur__nom", "matiere__nom")
