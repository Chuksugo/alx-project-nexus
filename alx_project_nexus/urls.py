"""
URL configuration for alx_project_nexus project.
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ========================================================
# API SCHEMA (Swagger / Redoc)
# ========================================================
schema_view = get_schema_view(
    openapi.Info(
        title="ALX Project Nexus API",
        default_version="v1",
        description="E-Commerce Backend API",
        contact=openapi.Contact(email="you@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ========================================================
# ROOT ENDPOINTS
# ========================================================
def home(request):
    """Root endpoint for sanity check."""
    return JsonResponse({"message": "Welcome to ALX Project Nexus API"})


def api_index(request):
    """API index endpoint providing main routes."""
    return JsonResponse({
        "auth": {
            "token": "/api/auth/token/",
            "refresh": "/api/auth/token/refresh/"
        },
        "products": "/api/products/",
        "accounts": "/api/accounts/",
        "orders": "/api/orders/",
        "docs": {
            "swagger": "/swagger/",
            "redoc": "/redoc/"
        }
    })

# ========================================================
# URL PATTERNS
# ========================================================
urlpatterns = [
    # Root
    path("", home, name="home"),
    path("api/", api_index, name="api_index"),

    # Admin
    path("admin/", admin.site.urls),

    # Authentication (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # App routes
    path("api/products/", include("products.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/orders/", include("orders.urls")),

    # Documentation
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
