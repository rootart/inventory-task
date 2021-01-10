from django.db import models
from django.utils import timezone

from inventory.constants import Freshness


class BatchQueryset(models.QuerySet):
    def in_stock(self):
        return self.filter(
            current_quantity__gt=0
        )

    def filter_by_freshness(self, kind: str):
        today = timezone.now().date()

        if kind == Freshness.FRESH:
            return self.filter(expiration_date__gt=today)
        elif kind == Freshness.EXPIRING_TODAY:
            return self.filter(expiration_date=today)
        elif kind == Freshness.EXPIRED:
            return self.filter(expiration_date__lt=today)

        return self
