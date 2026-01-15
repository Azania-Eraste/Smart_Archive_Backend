# dossiers/views.py
import io
import zipfile

from django.db.models import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document, Eleve
from .serializers import DocumentSerializer, EleveSerializer


class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()
    srializer_class = EleveSerializer
    permission_classes = [IsAuthenticated]

    # --- FILTRES ET RECHERCHE ---
    # Indispensable pour la barre de recherche du frontend
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtres exacts (ex: ?classe=1&statut=ACTIF)
    filterset_fields = ["classe", "statut"]

    # Recherche texte (ex: ?search=Kouadio)
    search_fields = ["nom", "prenom", "matricule"]

    # Tri (ex: ?ordering=nom)
    ordering_fields = ["nom", "date_naissance"]

    @action(detail=True, methods=["get"])
    def documents(self, request, pk=None):
        """
        Récupère tous les documents d'un élève.
        Usage: GET /api/dossiers/eleves/{id}/documents/
        """
        try:
            eleve = self.get_object()
        except Eleve.DoesNotExist:
            return Response(
                {"detail": "Élève non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Récupère tous les documents de l'élève
        documents = eleve.documents.all()

        # Serialise les documents
        serializer = DocumentSerializer(documents, many=True)

        return Response(
            {
                "eleve": {
                    "id": eleve.id,
                    "matricule": eleve.matricule,
                    "nom": eleve.nom,
                    "prenom": eleve.prenom,
                    "date_naissance": eleve.date_naissance,
                },
                "count": documents.count(),
                "documents": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def download_zip(self, request, pk=None):
        """
        Télécharge tous les documents d'un élève dans un fichier ZIP.
        Usage: GET /api/dossiers/eleves/{id}/download_zip/
        """
        try:
            eleve = self.get_object()
        except Eleve.DoesNotExist:
            return Response(
                {"detail": "Élève non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Récupère tous les documents de l'élève
        documents = eleve.documents.all()

        if not documents.exists():
            return Response(
                {"detail": "Cet élève n'a aucun document à télécharger."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Crée un buffer en mémoire pour le ZIP
        zip_buffer = io.BytesIO()

        try:
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for doc in documents:
                    # Vérifie que le fichier existe physiquement
                    if doc.fichier and hasattr(doc.fichier, "path"):
                        try:
                            # Construit un nom propre pour le fichier dans le ZIP
                            file_name = (
                                f"{doc.get_type_document_display()}_{doc.titre}.pdf"
                            )
                            # Nettoie le nom pour éviter les caractères invalides
                            file_name = "".join(
                                c
                                for c in file_name
                                if c.isalnum() or c in (" ", "_", "-", ".")
                            ).strip()

                            # Ajoute le fichier au ZIP
                            zip_file.write(doc.fichier.path, arcname=file_name)
                        except Exception as e:
                            print(e)
                            pass

            # Remet le curseur au début du buffer
            zip_buffer.seek(0)

            # Retourne le ZIP en tant que pièce jointe
            response = HttpResponse(
                zip_buffer.getvalue(), content_type="application/zip"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="dossier_{eleve.matricule}.zip"'
            )
            return response

        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la création du ZIP: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="annee")
    def annee(self, request, pk=None):
        """
        Récupère les années scolaires présentes dans les documents d'un élève.
        Usage: GET /api/dossiers/eleves/{id}/annee/
        Retourne une liste d'années avec le nombre de documents par année.
        """
        try:
            eleve = self.get_object()
        except Eleve.DoesNotExist:
            return Response(
                {"detail": "Élève non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Regroupe les documents par année scolaire
        years = (
            Document.objects.filter(eleve=eleve, annee_scolaire__isnull=False)
            .values("annee_scolaire__id", "annee_scolaire__libelle")
            .annotate(count=Count("id"))
            .order_by("-annee_scolaire__id")
        )

        # Formate la réponse
        data = [
            {
                "id": y["annee_scolaire__id"],
                "libelle": y["annee_scolaire__libelle"],
                "count": y["count"],
            }
            for y in years
        ]

        return Response(
            {"eleve_id": eleve.id, "annees": data}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get"], url_path=r"annee/(?P<annee_id>[^/.]+)")
    def annee_documents(self, request, pk=None, annee_id=None):
        """
        Récupère tous les documents d'un élève pour une année scolaire donnée.
        Usage: GET /api/dossiers/eleves/{id}/annee/{annee_id}/
        """
        try:
            eleve = self.get_object()
        except Eleve.DoesNotExist:
            return Response(
                {"detail": "Élève non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Filtre les documents par élève et année
        documents = Document.objects.filter(
            eleve=eleve, annee_scolaire__id=annee_id
        ).order_by("-date_upload")

        if not documents.exists():
            return Response(
                {"detail": "Aucun document trouvé pour cette année."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DocumentSerializer(documents, many=True)

        # Récupère quelques infos sur l'année
        annee_obj = None
        if documents[0].annee_scolaire:
            annee_obj = {
                "id": documents[0].annee_scolaire.id,
                "libelle": documents[0].annee_scolaire.libelle,
            }

        return Response(
            {
                "eleve": {
                    "id": eleve.id,
                    "matricule": eleve.matricule,
                    "nom": eleve.nom,
                    "prenom": eleve.prenom,
                },
                "annee": annee_obj,
                "count": documents.count(),
                "documents": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    # --- CONFIGURATION UPLOAD ---
    # Ces parsers permettent de gérer les requêtes "multipart/form-data"
    # (c'est le format standard pour envoyer des fichiers)
    parser_classes = (MultiPartParser, FormParser)

    # --- FILTRES ET RECHERCHE ---
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Filtres exacts
    filterset_fields = ["annee_scolaire", "type_document", "eleve"]

    # Recherche texte
    search_fields = ["titre", "eleve__nom", "eleve__prenom"]

    def perform_create(self, serializer):
        # Vous pouvez ajouter de la logique ici avant de sauvegarder
        # Par exemple, vérifier que l'utilisateur a le droit d'ajouter ce document
        serializer.save()


class DashboardStatsView(APIView):
    """
    Vue API pour les statistiques du dashboard.
    Endpoint: GET /api/dossiers/stats/

    Retourne un dictionnaire avec des statistiques globales sur les élèves et documents.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retourne les statistiques du système.
        """
        # Compte total d'élèves
        total_eleves = Eleve.objects.count()

        # Compte total de documents
        total_documents = Document.objects.count()

        # Élèves sans acte de naissance
        eleves_sans_acte = (
            Eleve.objects.exclude(
                documents__type_document=Document.TypeDocument.ACTE_NAISSANCE
            )
            .distinct()
            .count()
        )

        # Les 5 derniers documents uploadés
        recent_uploads = Document.objects.select_related("eleve").order_by(
            "-date_upload"
        )[:5]
        recent_uploads_data = [
            {
                "id": doc.id,
                "titre": doc.titre,
                "type": doc.get_type_document_display(),
                "eleve_nom": doc.eleve.nom,
                "eleve_prenom": doc.eleve.prenom,
                "date_upload": doc.date_upload,
            }
            for doc in recent_uploads
        ]

        # Documents par type
        documents_par_type = {}
        for choice_value, choice_display in Document.TypeDocument.choices:
            count = Document.objects.filter(type_document=choice_value).count()
            documents_par_type[choice_display] = count

        # Statistiques par statut d'élève
        eleves_par_statut = {}
        for choice_value, choice_display in Eleve.StatutEleve.choices:
            count = Eleve.objects.filter(statut=choice_value).count()
            eleves_par_statut[choice_display] = count

        return Response(
            {
                "total_eleves": total_eleves,
                "total_documents": total_documents,
                "eleves_sans_acte_naissance": eleves_sans_acte,
                "documents_par_type": documents_par_type,
                "eleves_par_statut": eleves_par_statut,
                "recent_uploads": recent_uploads_data,
            },
            status=status.HTTP_200_OK,
        )
