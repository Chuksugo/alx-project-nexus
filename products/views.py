from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Provides CRUD operations and uses slug as lookup field.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    Only active products are returned.
    Supports filtering, ordering, and search.
    """
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer

    # Filtering, ordering, and search configuration
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["category__id", "category__slug", "is_active"]
    ordering_fields = ["price", "created_at", "name"]
    search_fields = ["name", "description"]
