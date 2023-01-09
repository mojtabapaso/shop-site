from django.contrib import admin
from .models import Address, Order, Cart, Coupon
from .utils.create_coupon import create_coupon

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Cart)


@admin.action(description='فعال تخفیف')
def activer(modeladmin, request, queryset):
    queryset.update(code=str(create_coupon()), is_active=True)


@admin.action(description='غیر فعال تخفیف')
def deactiver(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    exclude = ("code ",)
    readonly_fields = ('code',)
    actions = (activer, deactiver)
