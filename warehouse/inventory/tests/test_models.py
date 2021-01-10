import pytest


@pytest.mark.django_db
class TestBatchModel:
    def test_stocked_quantity_property(self, batch_factory):
        batch = batch_factory()
        assert batch.distributions.count() == 0
        assert batch.declared_quantity == batch.stocked_quantity

    def test_stocked_quantity_property_with_distributions(
        self,
        batch_factory,
        distribution_factory
    ):
        batch = batch_factory(
            declared_quantity=100
        )
        distribution_factory(batch=batch, quantity=10)
        distribution_factory(batch=batch, quantity=20)
        assert batch.stocked_quantity == 100 - 20 - 10
