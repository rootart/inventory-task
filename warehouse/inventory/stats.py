from dataclasses import dataclass

from django.db.models import QuerySet, F

from inventory.constants import Freshness


@dataclass
class Overview:
    """
    Provides basic warehouse overview per product basis outlining in-stock batches by their freshness.
    """
    queryset: QuerySet

    def _batches(self):
        return self.queryset.in_stock()

    def products(self):
        products = list(
            self
            ._batches()
            .annotate(
                title=F('product__title'),
            )
            .values('title', 'product_id').distinct()
        )
        for product in products:
            product['freshness'] = {}
            for kind, _ in Freshness.CHOICES:
                product['freshness'][kind] = (
                    self
                    ._batches()
                    .filter(product_id=product['product_id'])
                    .filter_by_freshness(kind)
                    .count()
                )

        return products
