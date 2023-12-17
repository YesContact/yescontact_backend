from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Pastebin API",
        default_version="v1",
        description="API for Pastebin",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("user/", include("users.urls.views"), name="user"),
    path("api/", include("users.urls.apis"), name="api"),
    path("core/", include("core.urls"), name="core"),
    path("survey-api/", include("survey.urls"), name="survey"),
    path(
        "api-docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
