from django.contrib import admin

from inventory.models import (
    Batch,
    Distribution,
    Product,
)

admin.site.register(Product)
admin.site.register(Batch)
admin.site.register(Distribution)
