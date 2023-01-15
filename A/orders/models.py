from django.db import models
from django.contrib.auth import get_user_model
from products.models import Products
from django_jalali.db import models as jmodels

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='cart_user')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        # show total price
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price() + self.get_total_item_price()

    class Meta:
        verbose_name_plural = "سبد خرید"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    items = models.ManyToManyField(Cart, verbose_name='محصول')
    start_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ خرید')
    ordered_date = jmodels.jDateTimeField(verbose_name='تاریخ سفارش')
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده است')
    address = models.CharField(max_length=500, verbose_name='آدرس', )
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='کد تخفیف')
    received = models.BooleanField(default=False, verbose_name='تحویل داده شده')
    refund_requested = models.BooleanField(default=False, verbose_name='درخواست بازگشت پول ')
    refund_granted = models.BooleanField(default=False, verbose_name='درخواست پول انجام شده')

    def __str__(self):
        return f"{self.user.first_name}  - {self.user.last_name}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    class Meta:
        verbose_name_plural = "سفارش"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_user')
    address = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'آدرس ها'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='related_in_coupon')
    code = models.CharField(max_length=15, null=True, blank=True, help_text="Auto dont input any thing")
    amount = models.IntegerField(verbose_name='مقدار', null=True, blank=True)
    min_order = models.IntegerField(verbose_name='حداقل سفارش ', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    create = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')
    expiry = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ انتضا')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف ها '
#
# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     accepted = models.BooleanField(default=False)
#     email = models.EmailField()
#
#     def __str__(self):
#         return f"{self.pk}"
