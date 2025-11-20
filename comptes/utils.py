# comptes/utils.py
from django.apps import apps


def generer_nouveau_matricule(instance, role_prefix):
    """
    Génère un matricule au format : ECO-ROLE-NOMPRE-001
    Ex: IIT-PRO-KOUAZA-001
    """
    # 1. Récupérer le trigramme de l'établissement
    # On utilise get_model pour éviter les imports circulaires
    Ecole = apps.get_model("etablissement", "Ecole")
    ecole = Ecole.objects.first()

    if ecole and ecole.nom:
        # Prend les 3 premières lettres, en majuscules, sans espaces
        prefix_ecole = ecole.nom.replace(" ", "")[:3].upper()
    else:
        prefix_ecole = "ECO"  # Valeur par défaut si pas d'école créée

    # 2. Récupérer les trigrammes Nom/Prénom
    # instance.utilisateur est l'objet lié (pour Prof, Educateur...)
    # instance tout court pour Eleve (car nom/prenom sont directement dessus)
    if hasattr(instance, "utilisateur"):
        nom = instance.utilisateur.nom
        prenom = instance.utilisateur.prenom
    else:
        # Cas de l'élève
        nom = instance.nom
        prenom = instance.prenom

    # Nettoyage et formatage (3 lettres nom + 3 lettres prenom)
    tri_nom = nom.replace(" ", "")[:3].upper()
    tri_prenom = prenom.replace(" ", "")[:3].upper()

    racine = f"{prefix_ecole}-{role_prefix}-{tri_nom}{tri_prenom}"

    # 3. Gérer l'incrémentation (001, 002...)
    # On cherche tous les objets qui commencent par cette racine
    ModelClass = instance.__class__

    # On filtre sur la base de données pour voir combien existent déjà
    # startswith est parfait pour ça
    derniers_objets = ModelClass.objects.filter(matricule__startswith=racine).order_by(
        "matricule"
    )

    if not derniers_objets.exists():
        sequence = "001"
    else:
        # On prend le dernier, on extrait le numéro et on ajoute 1
        dernier_matricule = derniers_objets.last().matricule
        try:
            # Le numéro correspond aux 3 derniers caractères
            dernier_numero = int(dernier_matricule.split("-")[-1])
            sequence = f"{dernier_numero + 1:03d}"
        except ValueError:
            # Sécurité si le matricule manuel ne respecte pas le format
            sequence = f"{derniers_objets.count() + 1:03d}"

    return f"{racine}-{sequence}"
