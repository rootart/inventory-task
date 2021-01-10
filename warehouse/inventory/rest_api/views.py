from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)

from inventory.models import (
    Batch,
    Product,
)
from inventory.rest_api.serializers import (
    BatchSerializer,
    DistributionSerializer,
    ProductSerializer,
)


class ProductListApiView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailsApiView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'product_id'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class BatchListApiView(ListCreateAPIView):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()


class BatchDetailsApiView(RetrieveDestroyAPIView):
    lookup_url_kwarg = 'batch_id'
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()


class BatchDistributionListApiView(ListCreateAPIView):
    serializer_class = DistributionSerializer

    def dispatch(self, request, *args, **kwargs):
        batch_id = self.kwargs.get('batch_id')
        self.batch = Batch.objects.filter(id=batch_id).first()
        if not self.batch:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.batch.distributions.all()

    def get_serializer_context(self):
        return {
            'batch': getattr(self, 'batch', None),
        }

    @swagger_auto_schema(
        request_body=DistributionSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
