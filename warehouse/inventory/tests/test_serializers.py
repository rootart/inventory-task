from datetime import timedelta

from django.utils import timezone
import factory as factory_boy
import pytest

from inventory.constants import DistributionType
from inventory.rest_api.serializers import (
    BatchSerializer,
    DistributionSerializer,
)


@pytest.fixture
def batch_dict(batch_factory):
    dict_data = factory_boy.build(dict, FACTORY_CLASS=batch_factory)
    product = dict_data['product']
    product.save()
    dict_data['product'] = product.id
    return dict_data


@pytest.mark.django_db
class TestBatchSerializer:
    def test_creation(self, batch_dict):
        serializer = BatchSerializer(data=batch_dict)
        assert serializer.is_valid()
        serializer.save()
        assert serializer.instance.current_quantity
        assert serializer.instance.current_quantity == serializer.instance.stocked_quantity

    @pytest.mark.parametrize(
        "expiration_date,is_valid",
        [
            ((timezone.now() - timedelta(days=0)).date(), False),
            ((timezone.now() - timedelta(days=1)).date(), False),
            ((timezone.now() + timedelta(days=1)).date(), True),
        ]
    )
    def test_expiration_date_validation(self, expiration_date, is_valid, batch_dict):
        batch_dict['expiration_date'] = expiration_date
        serializer = BatchSerializer(data=batch_dict)
        assert serializer.is_valid() is is_valid
        if not is_valid:
            assert 'expiration_date' in serializer.errors


@pytest.mark.django_db
class TestDistributionSerializer:
    def test_quantity_validation(self, batch_factory):
        batch = batch_factory()
        data = {
            'quantity': batch.stocked_quantity + 1,
            'kind': DistributionType.SHIPMENT,
        }
        serializer = DistributionSerializer(
            data=data,
            context={
                'batch': batch,
            }
        )
        assert not serializer.is_valid()
        assert 'quantity' in serializer.errors
