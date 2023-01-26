from django.contrib import admin
from .models import Order, Cart, Coupon


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('items', 'user', 'address', 'ordered_date', 'ordered', 'all_price', 'price_pey', 'price_coupon')
    readonly_fields = ('items', 'user', 'ordered_date')


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
