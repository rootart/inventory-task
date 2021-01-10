from django.db import models


class DistributionType(models.TextChoices):
    SHIPMENT = 'shipment', 'Shipment'
    CORRECTION = 'correction', 'Correction'


# Freshness options
class Freshness:
    FRESH = 'fresh'
    EXPIRING_TODAY = 'expiring_today'
    EXPIRED = 'expired'
    CHOICES = (
        (FRESH, 'Fresh'),
        (EXPIRING_TODAY, 'Expiring today'),
        (EXPIRED, 'Expired'),
    )
