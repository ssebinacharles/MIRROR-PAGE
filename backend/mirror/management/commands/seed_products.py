from django.core.management.base import BaseCommand

from mirror.models import Product


PRODUCTS = [
    {
        "name": "Mirror DevStation 14",
        "description": "Compact development laptop for software engineering and cloud work.",
        "category": "developer-laptop",
        "price": "899.00",
        "currency": "USD",
        "specs": {
            "cpu": "8-core",
            "ram": "16GB",
            "storage": "512GB NVMe",
            "gpu": "Integrated",
        },
    },
    {
        "name": "Mirror DevStation 15",
        "description": "Balanced development laptop for backend engineering and data workloads.",
        "category": "developer-laptop",
        "price": "1099.00",
        "currency": "USD",
        "specs": {
            "cpu": "12-core",
            "ram": "32GB",
            "storage": "1TB NVMe",
            "gpu": "Integrated",
        },
    },
    {
        "name": "Mirror ComputeBook 16",
        "description": "High-performance development workstation for demanding workloads.",
        "category": "developer-laptop",
        "price": "1399.00",
        "currency": "USD",
        "specs": {
            "cpu": "16-core",
            "ram": "64GB",
            "storage": "2TB NVMe",
            "gpu": "Dedicated",
        },
    },
    {
        "name": "Mirror LiteDev 13",
        "description": "Lightweight programming laptop for everyday development.",
        "category": "developer-laptop",
        "price": "749.00",
        "currency": "USD",
        "specs": {
            "cpu": "6-core",
            "ram": "16GB",
            "storage": "512GB NVMe",
            "gpu": "Integrated",
        },
    },
]


class Command(BaseCommand):
    help = "Seed the MIRROR synthetic product catalog."

    def handle(self, *args, **options):
        for data in PRODUCTS:
            Product.objects.update_or_create(
                name=data["name"],
                defaults=data,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(PRODUCTS)} MIRROR products."
            )
        )
