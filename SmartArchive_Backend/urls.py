# systeme_archivage/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# --- IMPORTS SWAGGER ---
from rest_framework import permissions

# --- CONFIGURATION SWAGGER ---
schema_view = get_schema_view(
    openapi.Info(
        title="SmartArchive API",
        default_version="v1",
        description="Documentation de l'API pour le système d'archivage scolaire",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@smartarchive.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- VOS API ---
    path("api/comptes/", include("comptes.urls")),
    path("api/etablissement/", include("etablissement.urls")),
    path("api/dossiers/", include("dossiers.urls")),
    path("api/pedagogie/", include("pedagogie.urls")),
    path("api/inscriptions/", include("inscriptions.urls")),
    # --- ROUTES DOCUMENTATION ---
    # Le fichier JSON brut (utile pour les outils externes)
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    # L'interface graphique Swagger (La plus utilisée)
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Une autre interface (Redoc), plus propre pour la lecture seule
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
