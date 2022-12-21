from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from pages.models import Category
from ckeditor.fields import RichTextField


class Brand(models.Model):
    category = models.ManyToManyField(Category, related_name='brand')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name_plural = "نام تجاری"

    def __str__(self):
        return self.name


class Products(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    slug = models.SlugField()
    description_long = RichTextField()
    image = models.ImageField(upload_to='static/img')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:product_detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("pages:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("pages:remove-from-cart", kwargs={'slug': self.slug})


class Commend(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = RichTextField()
    create = jmodels.jDateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}--{self.body[:30]}----{self.active}'

#
# class LikeAndDislike(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
#     comment = models.OneToOneField(Commend, on_delete=models.CASCADE)
#     # like = models.
