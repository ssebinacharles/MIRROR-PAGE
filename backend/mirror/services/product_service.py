from __future__ import annotations

from django.db.models import Q

from mirror.models import Product


def search_products(query: str, max_price=None):
    queryset = Product.objects.filter(available=True)
    query = (query or "").strip()

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__icontains=query)
        )

    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    return queryset.order_by("price", "name")


def get_product(product_id: str):
    return Product.objects.filter(id=product_id, available=True).first()
