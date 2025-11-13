# inscriptions/models.py

from django.conf import settings  # Pour lier à l'utilisateur qui traite
from django.db import models

# On importe les modèles des autres applications
from dossiers.models import Document, Eleve
from etablissement.models import AnneeScolaire, Classe

# --- 1. Modèle Inscription ---
# Gère la demande d'inscription ou de réinscription pour un élève


class Inscription(models.Model):

    # L'élève concerné par cette demande d'inscription
    # Nous utilisons OneToOneField pour s'assurer qu'il n'y a qu'une
    # demande d'inscription par élève et par an (voir Meta unique_together)
    eleve = models.ForeignKey(
        Eleve, on_delete=models.CASCADE, related_name="inscriptions"
    )

    # La classe dans laquelle l'élève est (ou sera) inscrit
    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,  # On garde la demande même si la classe est supprimée
        null=True,
    )

    annee_scolaire = models.ForeignKey(
        AnneeScolaire,
        on_delete=models.PROTECT,  # Empêcher la suppression d'une année si des inscriptions y sont liées
        related_name="inscriptions",
    )

    # Statut du processus (UC2)
    class StatutInscription(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente de validation"
        APPROUVEE = "APPROUVEE", "Approuvée"
        REJETEE = "REJETEE", "Rejetée"
        INCOMPLET = "INCOMPLET", "Dossier incomplet"

    statut = models.CharField(
        max_length=50,
        choices=StatutInscription.choices,
        default=StatutInscription.INCOMPLET,
    )

    date_demande = models.DateTimeField(auto_now_add=True)

    # Qui a traité cette demande (Secrétaire ou Educateur)
    traitee_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilise le modèle Utilisateur (comptes.Utilisateur)
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Suivi financier
    frais_inscription = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )

    # Rattachement des pièces justificatives (UC2)
    # Quand l'éducateur/secrétaire uploade un Document (via l'app 'dossiers'),
    # on peut le lier ici pour confirmer qu'il a été fourni *pour cette inscription*.
    documents_fournis = models.ManyToManyField(
        Document, blank=True, related_name="inscriptions_associees"
    )

    notes_administratives = models.TextField(blank=True, null=True)

    class Meta:
        # Un élève ne peut avoir qu'une seule demande d'inscription par année scolaire
        unique_together = ("eleve", "annee_scolaire")

    def __str__(self):
        return f"Inscription de {self.eleve.nom} pour {self.annee_scolaire} ({self.get_statut_display()})"
