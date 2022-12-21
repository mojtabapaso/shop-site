from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels
from products.models import Products
from django_countries.fields import CountryField



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    # show total price
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    # Calculate the amount of the discount if available

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    # Calculate the final price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    # The final price will be received and if there is a discount, it will be calculated


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='نام کاربر')
    # ref_code = models.CharField(max_length=20,verbose_name='')
    items = models.ManyToManyField(OrderItem, verbose_name='محصول')
    start_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ خرید')
    ordered_date = jmodels.jDateTimeField(verbose_name='تاریخ سفارش')
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده است')
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='billing_address', verbose_name='آدرس')
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='کد تخفیف')

    received = models.BooleanField(default=False, verbose_name='تحویل داده شده')
    # refund
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


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}  - {self.user.last_name}"

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
