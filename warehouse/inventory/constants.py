from django.db import models


class DistributionType(models.TextChoices):
    SHIPMENT = 'shipment', 'Shipment'
    CORRECTION = 'correction', 'Correction'
