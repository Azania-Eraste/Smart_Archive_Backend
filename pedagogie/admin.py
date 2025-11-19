from django.contrib import admin

from .models import Bulletin, Evaluation, Note


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("titre", "matiere_display", "classe_display", "date", "coefficient")
    list_filter = ("enseignement__matiere", "enseignement__classe", "date")
    search_fields = ("titre", "enseignement__professeur__utilisateur__nom")

    # Fonctions pour afficher les infos liées (via Enseignement)
    @admin.display(description="Matière")
    def matiere_display(self, obj):
        return obj.enseignement.matiere.nom

    @admin.display(description="Classe")
    def classe_display(self, obj):
        return str(obj.enseignement.classe)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("eleve", "valeur", "evaluation", "date_saisie")
    list_filter = ("evaluation", "date_saisie")
    search_fields = ("eleve__nom", "eleve__matricule")


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ("eleve", "trimestre", "annee_scolaire", "moyenne_generale")
    list_filter = ("trimestre", "annee_scolaire", "eleve__classe")
    search_fields = ("eleve__nom",)
