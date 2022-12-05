from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order_user')
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(default=None)
    created = jmodels.jDateTimeField(auto_now=True)
    updated = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.paid}'

    class Meta:
        ordering = ('paid', 'user')


class OrderItem(models.Model):
    pass
