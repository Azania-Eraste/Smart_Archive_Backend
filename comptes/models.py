# comptes/models.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# --- 1. Le Manager pour notre Utilisateur Personnalisé ---
# Django a besoin d'un "Manager" pour savoir COMMENT créer des utilisateurs et des super-utilisateurs.


class UtilisateurManager(BaseUserManager):
    """Manager pour le modèle Utilisateur."""

    def create_user(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        """Crée et sauvegarde un nouvel utilisateur."""
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email.")

        email = self.normalize_email(email)
        utilisateur = self.model(email=email, nom=nom, prenom=prenom, **extra_fields)
        utilisateur.set_password(mot_de_passe)
        utilisateur.save(using=self._db)
        return utilisateur

    def create_superuser(self, email, nom, prenom, mot_de_passe):
        """Crée et sauvegarde un super-utilisateur."""
        utilisateur = self.create_user(email, nom, prenom, mot_de_passe)
        utilisateur.is_staff = True
        utilisateur.is_superuser = True
        utilisateur.save(using=self._db)
        return utilisateur


# --- 2. Le Modèle Utilisateur de Base ---
# C'est le modèle qui gérera l'authentification (login)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Modèle de base pour tous les utilisateurs du système."""

    # On utilise l'email comme identifiant unique au lieu d'un "username"
    email = models.EmailField(max_length=255, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permet l'accès à l'admin Django

    # Types de rôles (pour savoir quel profil charger)
    # C'est plus propre que de simples strings
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"  # Directeur, Fondateur
        SECRETAIRE = "SECRETAIRE", "Secrétaire"
        EDUCATEUR = "EDUCATEUR", "Educateur"
        PROFESSEUR = "PROFESSEUR", "Professeur"
        PARENT = "PARENT", "Parent"

    # Le rôle de base de l'utilisateur
    role = models.CharField(max_length=50, choices=Roles.choices)

    # On dit à Django d'utiliser notre Manager
    objects = UtilisateurManager()

    # On définit le champ de login
    USERNAME_FIELD = "email"
    # Champs requis lors de la création d'un super-utilisateur
    REQUIRED_FIELDS = ["nom", "prenom"]

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def __str__(self):
        return self.email


# --- 3. Les Modèles de Profils (Rôles) ---
# Chaque rôle aura des informations spécifiques. On les lie à l'utilisateur de base.


class Parent(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    # On liera les élèves ici plus tard

    def __str__(self):
        return self.utilisateur.get_full_name()


class Professeur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    matricule = models.CharField(max_length=50, unique=True)
    # On liera les matières enseignées ici plus tard

    def __str__(self):
        return self.utilisateur.get_full_name()


class Educateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    matricule = models.CharField(max_length=50, unique=True)
    # On liera les classes gérées ici plus tard

    def __str__(self):
        return self.utilisateur.get_full_name()


class Secrétaire(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    matricule = models.CharField(max_length=50, unique=True)
    bureau = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.utilisateur.get_full_name()


class Directeur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    matricule = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.utilisateur.get_full_name()


class Fondateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True
    )
    matricule = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.utilisateur.get_full_name()
