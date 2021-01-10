from datetime import timedelta
import uuid

from django.utils import timezone
import factory as factory_boy

from inventory.constants import DistributionType
from inventory.models import (
    Batch,
    Distribution,
    Product,
)


class ProductFactory(factory_boy.django.DjangoModelFactory):
    title = factory_boy.Faker('name')
    code = factory_boy.LazyFunction(lambda: uuid.uuid4())

    class Meta:
        model = Product


class BatchFactory(factory_boy.django.DjangoModelFactory):
    product = factory_boy.SubFactory(ProductFactory)
    declared_quantity = 100
    current_quantity = factory_boy.LazyAttribute(lambda o: o.declared_quantity)
    delivery_timestamp = factory_boy.LazyFunction(lambda: timezone.now())
    expiration_date = factory_boy.LazyAttribute(
        lambda o: (o.delivery_timestamp + timedelta(days=7)).date()
    )

    class Meta:
        model = Batch


class DistributionFactory(factory_boy.django.DjangoModelFactory):
    batch = factory_boy.SubFactory(BatchFactory)
    kind = DistributionType.SHIPMENT
    quantity = 1

    class Meta:
        model = Distribution
