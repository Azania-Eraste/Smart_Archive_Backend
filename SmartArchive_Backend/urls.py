# systeme_archivage/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- NOS API ---
    path("api/comptes/", include("comptes.urls")),
    path("api/etablissement/", include("etablissement.urls")),
    path("api/dossiers/", include("dossiers.urls")),
    path("api/inscriptions/", include("inscriptions.urls")),
    path("api/pedagogie/", include("pedagogie.urls")),
]

# Pour servir les fichiers uploadés (Images, PDF) en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
