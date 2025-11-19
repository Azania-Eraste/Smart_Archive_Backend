from django.contrib import admin

from .models import Inscription


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    # On affiche les infos clés
    list_display = (
        "eleve",
        "classe",
        "annee_scolaire",
        "statut",
        "frais_inscription",
        "date_demande",
    )

    # Permet de modifier le statut directement depuis la liste !
    list_editable = ("statut", "frais_inscription")

    list_filter = ("statut", "annee_scolaire", "classe", "date_demande")
    search_fields = ("eleve__nom", "eleve__prenom", "eleve__matricule")

    # Empêcher la modification de la date de demande
    readonly_fields = ("date_demande",)

    # Sélectionner les documents sera plus joli avec un filtre horizontal
    filter_horizontal = ("documents_fournis",)
