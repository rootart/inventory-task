from django.contrib import admin
from django.urls import (
    include,
    path,
    re_path,
)

from inventory.views import schema_view

urlpatterns = [
    re_path(
        r'^docs(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path('api/warehouse/', include('inventory.urls')),
    path('admin/', admin.site.urls),
]
