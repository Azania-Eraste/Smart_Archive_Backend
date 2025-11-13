# dossiers/models.py

from django.db import models

# On importe les modèles des autres applications
from comptes.models import Parent
from etablissement.models import Classe

# --- 1. Modèle Eleve ---
# C'est l'entité centrale de l'archivage.


class Eleve(models.Model):
    # Lien vers la classe (administrative)
    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,  # Si on supprime la classe, on garde l'élève
        null=True,
        blank=True,
        related_name="eleves",
    )

    # Lien vers le(s) tuteur(s) (modèle Parent de l'app 'comptes')
    parents = models.ManyToManyField(Parent, blank=True, related_name="enfants")

    # Informations de base
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    # Statut de l'élève
    class StatutEleve(models.TextChoices):
        ACTIF = "ACTIF", "Actif"
        ARCHIVE = "ARCHIVE", "Archivé"  # Ancien élève
        RADIE = "RADIE", "Radié"

    statut = models.CharField(
        max_length=50, choices=StatutEleve.choices, default=StatutEleve.ACTIF
    )

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"


# --- 2. Modèle Document ---
# C'est le fichier d'archive (PDF, JPG...)


class Document(models.Model):
    # Lien vers l'élève à qui appartient ce document
    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE,  # Si on supprime l'élève, on supprime ses documents
        related_name="documents",
    )

    # Métadonnées (très important pour la recherche)
    titre = models.CharField(max_length=255)

    class TypeDocument(models.TextChoices):
        ACTE_NAISSANCE = "ACTE_NAISSANCE", "Acte de naissance"
        RECU = "RECU", "Reçu de paiement"
        DIPLOME_ANTERIEUR = "DIPLOME_ANTERIEUR", "Diplôme antérieur"
        PHOTO = "PHOTO", "Photo d'identité"
        AUTRE = "AUTRE", "Autre"

    type_document = models.CharField(
        max_length=50, choices=TypeDocument.choices, default=TypeDocument.AUTRE
    )

    annee_scolaire = models.CharField(max_length=9, blank=True)  # ex: "2024-2025"

    # Le fichier lui-même
    # 'uploads/documents/' sera le dossier où les fichiers sont stockés
    fichier = models.FileField(upload_to="uploads/documents/")
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.eleve.nom})"
