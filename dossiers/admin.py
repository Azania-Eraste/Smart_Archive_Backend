from django.contrib import admin

from .models import Document, Eleve


@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "classe", "statut")
    list_filter = (
        "statut",
        "classe__niveau",
        "classe",
    )  # Filtre par niveau puis par classe
    search_fields = ("matricule", "nom", "prenom")
    ordering = ("nom",)

    # Optimisation pour charger la classe plus vite
    list_select_related = ("classe",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("titre", "type_document", "eleve", "annee_scolaire", "date_upload")
    list_filter = ("type_document", "annee_scolaire", "date_upload")
    search_fields = ("titre", "eleve__nom", "eleve__matricule")

    # Pour voir le fichier directement dans la liste (lien cliquable)
    def fichier_link(self, obj):
        if obj.fichier:
            return obj.fichier.url
        return ""
