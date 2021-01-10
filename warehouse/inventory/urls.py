from django.urls import path

from inventory.rest_api import views as api_views

urlpatterns = [
    path(
        'overview/',
        api_views.WarehouseOverviewApiView.as_view(),
        name='api-warehouse-overview',
    ),
    path(
        'products/',
        api_views.ProductListApiView.as_view(),
        name='api-products-list'
    ),
    path(
        'products/<int:product_id>/',
        api_views.ProductDetailsApiView.as_view(),
        name='api-product-details'
    ),
    path(
        'batches/',
        api_views.BatchListApiView.as_view(),
        name='api-batches-list'
    ),
    path(
        'batches/<int:batch_id>/',
        api_views.BatchDetailsApiView.as_view(),
        name='api-batch-details'
    ),
    path(
        'batches/<int:batch_id>/distributions/',
        api_views.BatchDistributionListApiView.as_view(),
        name='api-batch-distributions-list'
    ),
]
