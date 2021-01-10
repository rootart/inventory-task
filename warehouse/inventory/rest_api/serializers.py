from django.utils import timezone
from rest_framework import serializers

from inventory.models import (
    Batch,
    Distribution,
    Product,
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'code',
        )


class BatchSerializer(serializers.ModelSerializer):
    stocked_quantity = serializers.SerializerMethodField()
    product_title = serializers.CharField(
        read_only=True,
        source='product.title'
    )

    class Meta:
        model = Batch
        fields = (
            'id',
            'product',
            'product_title',
            'declared_quantity',
            'stocked_quantity',
            'delivery_timestamp',
            'expiration_date',
            'created',
            'modified',

        )
        read_only_fields = (
            'created',
            'modified',
        )

    def get_stocked_quantity(self, instance: Batch):
        return instance.stocked_quantity

    def save(self, **kwargs):
        super().save(**kwargs)
        self.instance.current_quantity = self.instance.stocked_quantity
        self.instance.save(update_fields=['current_quantity', ])

    def validate_expiration_date(self, value):
        if timezone.now().date() >= value:
            raise serializers.ValidationError('Expiration date must be set in future.')
        return value


class BatchDetailsSerializer(BatchSerializer):
    has_distributions = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = BatchSerializer.Meta.fields + (
            'has_distributions',
        )

    def get_has_distributions(self, obj: Batch) -> bool:
        '''
        Indicates whether give batch has any distributions and could work as optimisation for further calls
        '''
        return obj.distributions.exists()


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = (
            'id',
            'kind',
            'quantity',
            'created',
            'modified',
        )
        read_only_fields = (
            'created',
            'modified',
        )

    def validate_quantity(self, value: int):
        batch: Batch = self.context['batch']
        stocked_quantity = batch.stocked_quantity
        if stocked_quantity < value:
            raise serializers.ValidationError(
                f'Distribution quantity of {value} exceeds existing amount of {stocked_quantity}'
            )
        return value

    def save(self, **kwargs):
        batch = self.context['batch']
        self.validated_data['batch_id'] = batch.id
        return super().save(**kwargs)


class WarehouseOverviewSerializer(serializers.Serializer):
    products = serializers.ListField()
