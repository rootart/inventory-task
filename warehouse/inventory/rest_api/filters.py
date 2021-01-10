from typing import List

from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework as filters

from inventory.constants import Freshness
from inventory.models import Batch


def filter_freshness(queryset, name: str, value: List[str]):
    """
    Implements filtering of the batches based on the expiration date.
    """
    today = timezone.now().date()
    query = Q()
    for option in set(value):
        if option == Freshness.FRESH:
            query |= Q(expiration_date__gt=today)
        elif option == Freshness.EXPIRING_TODAY:
            query |= Q(expiration_date=today)
        elif option == Freshness.EXPIRED:
            query |= Q(expiration_date__lt=today)
    return queryset.filter(query)


def filter_in_stock_only(queryset, name: str, value: bool):
    '''
    Filters only batches which are still available in warehouse
    '''
    if value:
        queryset = queryset.filter(current_quantity__gt=0)
    return queryset


class BatchFilterSet(filters.FilterSet):
    freshness = filters.MultipleChoiceFilter(
        choices=Freshness.CHOICES,
        field_name='freshness',
        method=filter_freshness,
    )
    in_stock_only = filters.BooleanFilter(
        field_name='in_stock_only',
        method=filter_in_stock_only,
    )

    class Meta:
        model = Batch
        fields = (
            'product',
            'freshness',
            'in_stock_only',
        )
