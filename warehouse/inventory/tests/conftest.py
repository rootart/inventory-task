from pytest_factoryboy import register

from inventory.tests import factories

register(factories.ProductFactory)
register(factories.BatchFactory)
register(factories.DistributionFactory)
