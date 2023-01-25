from django.contrib import admin
from .models import Order, Cart, Coupon


# admin.site.register(Address)
# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("items",)


admin.site.register(Cart)


@admin.action(description='فعال تخفیف')
def activer(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='غیر فعال تخفیف')
def deactiver(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    exclude = ("code ",)
    readonly_fields = ('code',)
    actions = (activer, deactiver)
