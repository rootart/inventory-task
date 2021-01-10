from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import (
    Batch,
    Product,
)
from inventory.rest_api.filters import BatchFilterSet
from inventory.rest_api.serializers import (
    BatchSerializer,
    DistributionSerializer,
    ProductSerializer,
    BatchDetailsSerializer, WarehouseOverviewSerializer,
)
from inventory.stats import Overview


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
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = BatchFilterSet


class BatchDetailsApiView(RetrieveDestroyAPIView):
    lookup_url_kwarg = 'batch_id'
    serializer_class = BatchDetailsSerializer
    queryset = Batch.objects.all()


class BatchDistributionListApiView(ListCreateAPIView):
    serializer_class = DistributionSerializer

    def dispatch(self, request, *args, **kwargs):
        batch_id = self.kwargs.get('batch_id')
        self.batch = Batch.objects.filter(id=batch_id).first()
        if not self.batch:
            self.headers = self.default_response_headers
            response = self.handle_exception(exceptions.NotFound('Not found'))
            response = self.finalize_response(request, response, *args, **kwargs)
            return response
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


class WarehouseOverviewApiView(APIView):
    serializer_class = WarehouseOverviewSerializer

    def get(self, request, format=None):
        stats_overview = Overview(
            Batch.objects.all()
        )
        serializer = self.serializer_class(stats_overview)
        return Response(serializer.data)
