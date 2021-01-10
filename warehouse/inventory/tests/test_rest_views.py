from datetime import timedelta
from urllib.parse import urlencode

from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone
import pytest

from inventory.constants import Freshness
from inventory.models import Batch


@pytest.mark.django_db
class TestBatchList:
    def test_filtering_by_product(self, batch_factory, client):
        product_1 = batch_factory()
        product_2 = batch_factory()  # noqa: F841
        filter_arguments = {
            'product': product_1.id,
        }
        url = reverse('api-batches-list') + '?' + urlencode(filter_arguments)
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == product_1.id

    def test_filtering_by_freshness(self, batch_factory, client):
        expired_batch = batch_factory(
            expiration_date=(timezone.now() - timedelta(days=1)).date()
        )
        expires_today_batch = batch_factory(
            expiration_date=timezone.now().date()
        )
        fresh_batch = batch_factory(
            expiration_date=(timezone.now() + timedelta(days=2)).date()
        )
        filter_arguments = QueryDict('', mutable=True)
        filter_arguments.setlist('freshness', [Freshness.FRESH, Freshness.EXPIRED, ])

        url = reverse('api-batches-list') + '?' + filter_arguments.urlencode()
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        batch_ids = [batch['id'] for batch in data]
        assert expired_batch.id in batch_ids
        assert fresh_batch.id in batch_ids
        assert expires_today_batch.id not in batch_ids


@pytest.mark.django_db
class TestDistributionsList:
    def test_not_found(self, client):
        assert Batch.objects.count() == 0
        response = client.get(reverse('api-batch-distributions-list', args=(1,)))
        assert response.status_code == 404

    def test_with_no_distributions(self, client, batch_factory):
        batch = batch_factory()
        response = client.get(reverse('api-batch-distributions-list', args=(batch.id,)))
        assert response.json() == []

    def test_with_existing_distribution(self, distribution_factory, client):
        distribution = distribution_factory()
        response = client.get(reverse('api-batch-distributions-list', args=(distribution.batch.id,)))
        assert len(response.json()) == 1
        assert distribution.id == response.json()[0]['id']
