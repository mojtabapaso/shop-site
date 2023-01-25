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
        return f"{self.quantity}از{self.item.title}"

    def price_item(self):
        price = self.item.price * self.quantity
        return price

    # def user_total(self):
    #     user = self.user
    #     for _ in self.user:
    #         if user=

    class Meta:
        verbose_name_plural = "سبد خرید"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    items = models.ManyToManyField(Cart, verbose_name='محصولات')
    start_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    ordered_date = jmodels.jDateTimeField(verbose_name='تاریخ سفارش', null=True, blank=True)
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='آدرس')
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده است')
    all_price = models.IntegerField(verbose_name='کل ارزش خرید بدون تخفیف', null=True, blank=True)
    price_pey = models.IntegerField(verbose_name='کل مبلغ پرداخت شده', null=True, blank=True)
    price_coupon = models.IntegerField(verbose_name='مبلغ کد تخفیف', null=True, blank=True)
    received = models.BooleanField(default=False, verbose_name='تحویل داده شده')
    refund_requested = models.BooleanField(default=False, verbose_name='درخواست بازگشت پول ')
    refund_granted = models.BooleanField(default=False, verbose_name='درخواست پول انجام شده')
    # --------------
    __original_price = None
    __product_price = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_price = self.all_price
        self.__product_price = self.total()

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.all_price != self.__original_price:
            self.price_pey = None
            self.price_coupon = None
            # self.all_price = self.__original_price
        if self.all_price != self.total():
            self.all_price = self.total()
        super().save(force_insert, force_update, *args, **kwargs)
        #  -----
        self.__original_price = self.all_price
        self.__product_price = self.all_price

    def total(self):
        item = self.items.all()
        a = 0
        for i in item:
            a += i.item.price * i.quantity
        return a

    def __str__(self):
        return f"{self.user.phone_number}"

    # def total(self):
    #     tal = 0
    #     for i in self.items.all():
    #         # for _ in len(i):
    #         tal += i.item.price * i.quantity
    #         return tal

    class Meta:
        verbose_name_plural = "سفارش"


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='related_in_coupon')
    code = models.CharField(max_length=15, null=True, blank=True, help_text="Auto Dont Need To Add")
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
