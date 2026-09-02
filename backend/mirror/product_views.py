from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductSearchView(APIView):
    """
    Search the synthetic MIRROR product catalog.

    Expected request:

    POST /api/products/search/

    {
        "query": "developer laptop",
        "max_price": 1200
    }
    """

    def post(self, request, *args, **kwargs):
        query = str(
            request.data.get("query", "")
        ).strip()

        max_price = request.data.get(
            "max_price"
        )

        queryset = Product.objects.filter(
            available=True
        )

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__icontains=query)
            )

        if max_price is not None:
            try:
                queryset = queryset.filter(
                    price__lte=float(max_price)
                )
            except (TypeError, ValueError):
                return Response(
                    {
                        "error": {
                            "code": "INVALID_MAX_PRICE",
                            "message": (
                                "max_price must be a number."
                            ),
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        queryset = queryset.order_by("price")

        serializer = ProductSerializer(
            queryset,
            many=True,
        )

        return Response(
            {
                "count": queryset.count(),
                "products": serializer.data,
            }
        )


class ProductDetailView(APIView):
    """
    Retrieve a single synthetic MIRROR product.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(
                pk=pk,
                available=True,
            )
        except Product.DoesNotExist:
            return Response(
                {
                    "error": {
                        "code": "PRODUCT_NOT_FOUND",
                        "message": "Product not found.",
                    }
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(product)

        return Response(serializer.data)