from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Warehouse management",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email="vasyl@dizhak.com"),
      license=openapi.License(name="Copyright (C) Vasyl Dizhak"),
   ),
   public=True,
   permission_classes=[],
)
