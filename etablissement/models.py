# etablissement/models.py

from django.db import models

# On importe les modèles de l'application 'comptes' car on en a besoin
from comptes.models import Educateur, Professeur


# --- AJOUT : Modèle Abstrait pour l'Adresse ---
# Ce modèle n'aura pas sa propre table,
# ses champs seront ajoutés aux modèles qui en héritent.
class AdresseModel(models.Model):
    """Modèle abstrait pour les champs d'adresse partagés."""

    ville = models.CharField(max_length=100, unique=True)
    commune = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    pays = models.CharField(
        max_length=100, blank=True, null=True, default="Cote d'Ivoire"
    )

    class Meta:
        abstract = True  # Très important !


# --- AJOUT : Modèle pour le Niveau Scolaire ---
class Niveau(models.Model):
    nom = models.CharField(
        max_length=50, unique=True
    )  # ex: "6ème", "5ème", "Terminale"
    # L'ordre nous permet de trier les niveaux correctement
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre"]  # Toujours trier par ordre (6ème avant 5ème)

    def __str__(self):
        return self.nom


# --- 1. Modèle Ecole (MODIFIÉ) ---
# Hérite maintenant de AdresseModel
class Ecole(AdresseModel):
    nom = models.CharField(max_length=255)
    # Les champs 'ville', 'commune', 'pays' sont
    # automatiquement inclus grâce à l'héritage.

    def __str__(self):
        return self.nom


# --- 2. Modèle Classe (MODIFIÉ) ---
# Utilise maintenant une ForeignKey vers Niveau
class Classe(models.Model):
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, related_name="classes")

    # --- MODIFICATION ---
    # Au lieu d'un CharField, on lie au nouveau modèle Niveau
    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.PROTECT,  # Empêche de supprimer un niveau si des classes y sont liées
        related_name="classes",
    )
    # --- FIN MODIFICATION ---

    nom = models.CharField(max_length=50)  # ex: "A", "B", "C1"

    educateur_referent = models.ForeignKey(
        Educateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes_gerees",
    )

    def __str__(self):
        return f"{self.niveau.nom} {self.nom} ({self.ecole.nom})"


# --- 3. Modèle Matière ---
class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


# --- 4. Modèle d'Association (Enseignement) ---
class Enseignement(models.Model):
    professeur = models.ForeignKey(
        Professeur, on_delete=models.CASCADE, related_name="enseignements"
    )
    matiere = models.ForeignKey(
        Matiere, on_delete=models.CASCADE, related_name="enseignements"
    )
    classe = models.ForeignKey(
        Classe, on_delete=models.CASCADE, related_name="enseignements"
    )
    coefficient = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("professeur", "matiere", "classe")

    def __str__(self):
        return f"{self.professeur} enseigne {self.matiere} en {self.classe}"
