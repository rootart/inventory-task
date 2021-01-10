from datetime import timedelta
from functools import partial

from django.utils import timezone
import pytest

from inventory.constants import Freshness
from inventory.models import Batch
from inventory.rest_api.filters import filter_freshness


@pytest.mark.django_db
class TestFreshnessFilter:
    def test_expired_batch_filter(self, batch_factory):
        expired_batch = batch_factory(
            expiration_date=(timezone.now() - timedelta(days=1)).date()
        )
        queryset = Batch.objects.all()
        assert queryset.count() == 1

        test_filter = partial(filter_freshness, queryset=queryset, name='freshness')

        # test against fresh and expiring today options
        filtered_queryset = test_filter(value=[
                Freshness.FRESH,
                Freshness.EXPIRING_TODAY,
            ]
        )
        assert filtered_queryset.count() == 0

        # test against multiple same options
        filtered_queryset = test_filter(value=[
                Freshness.FRESH,
                Freshness.FRESH,
            ]
        )
        assert filtered_queryset.count() == 0

        # test against expired and fresh
        filtered_queryset = test_filter(value=[
            Freshness.FRESH,
            Freshness.EXPIRED,
        ]
        )
        assert filtered_queryset.count() == 1
        assert expired_batch in filtered_queryset
