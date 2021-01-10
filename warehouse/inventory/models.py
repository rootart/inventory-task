from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel

from inventory.constants import DistributionType


class Product(TimeStampedModel):
    title = models.CharField(
        'Product title',
        max_length=255
    )
    code = models.UUIDField(
        unique=True
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Batch(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='batches',
    )
    declared_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), ]
    )
    current_quantity = models.PositiveIntegerField(
        help_text='Normalised field to keep track of the current quantity in stock',
        default=0,
    )
    delivery_timestamp = models.DateTimeField(
        auto_now=True,
        editable=True
    )
    expiration_date = models.DateField()

    @property
    def stocked_quantity(self) -> int:
        distributed = self.distributions.all().aggregate(
            distributed=Sum('quantity')
        )['distributed'] or 0
        return self.declared_quantity - distributed

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f'{self.product.title} with amount {self.declared_quantity} on {self.delivery_timestamp}'


class Distribution(TimeStampedModel):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='distributions'
    )
    kind = models.CharField(
        'Distribution kind',
        max_length=25,
        choices=DistributionType.choices,
        default=DistributionType.SHIPMENT,
        db_index=True
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), ]
    )

    class Meta:
        verbose_name = 'Batch distribution'
        verbose_name_plural = 'Batch distributions'

    def __str__(self):
        return f'{self.batch}, {self.get_kind_display()} on {self.created}'
