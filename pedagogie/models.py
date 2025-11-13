# pedagogie/models.py

from django.db import models

from comptes.models import Professeur

# On importe les modèles des autres applications
from dossiers.models import Eleve
from etablissement.models import Classe, Enseignement, Matiere

# --- 1. Modèle Evaluation ---
# Définit un devoir, un examen ou une interrogation


class Evaluation(models.Model):
    titre = models.CharField(max_length=255)  # ex: "Devoir Sur Table N°1"
    date = models.DateField()

    # Lien vers le cours (Enseignement) concerné
    # C'est le lien le plus important. Il nous dit :
    # 1. Quel Professeur a créé l'évaluation
    # 2. Pour quelle Classe
    # 3. Pour quelle Matière
    enseignement = models.ForeignKey(
        Enseignement, on_delete=models.CASCADE, related_name="evaluations"
    )

    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"{self.titre} ({self.enseignement.classe} - {self.enseignement.matiere})"
        )


# --- 2. Modèle Note ---
# Stocke la note d'un élève pour une évaluation donnée


class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="notes")
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, related_name="notes"
    )

    valeur = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # Permet les notes comme 15.5
    appreciation = models.TextField(blank=True, null=True)  # Commentaire du professeur

    date_saisie = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un élève ne peut avoir qu'une seule note pour une évaluation
        unique_together = ("eleve", "evaluation")

    def __str__(self):
        return f"Note: {self.valeur} pour {self.eleve.nom} ({self.evaluation.titre})"


# --- 3. Modèle Bulletin (Optionnel mais recommandé) ---
# Pour stocker les moyennes calculées et le PDF généré


class Bulletin(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="bulletins")
    trimestre = models.PositiveIntegerField()  # 1, 2, ou 3
    annee_scolaire = models.CharField(max_length=9)  # ex: "2024-2025"

    moyenne_generale = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    appreciation_generale = models.TextField(blank=True, null=True)

    # Stocke le bulletin généré
    fichier_pdf = models.FileField(
        upload_to="uploads/bulletins/", null=True, blank=True
    )

    date_generation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("eleve", "trimestre", "annee_scolaire")

    def __str__(self):
        return (
            f"Bulletin T{self.trimestre} ({self.annee_scolaire}) pour {self.eleve.nom}"
        )
