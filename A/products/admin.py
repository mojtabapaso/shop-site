from django.contrib import admin
from .models import Brand, Laptop

admin.site.register(Brand)


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
