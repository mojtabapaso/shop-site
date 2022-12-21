from django.db.models import Q
from django.shortcuts import render, reverse, resolve_url, redirect
from django.views import View
from .models import Category
from products.models import Brand, Products
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from products.forms import CommendForm
from products.models import Commend
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    template_name = 'pages/index.html'

    def get(self, request, slug_category=None):
        categories = Category.objects.filter(is_sub_category=False)
        products = Products.objects.all()
        if slug_category:
            category = Category.objects.filter(slug=slug_category)
            products = Products.objects.filter(Q(category__in=category))
        return render(request, 'pages/index.html', {'products': products, 'categories': categories})


class ProductsDetailView(LoginRequiredMixin, View):
    template_name = 'pages/detail.html'
    form_class = CommendForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Products, slug=kwargs['slug'])
        self.commend = Commend.objects.filter(active=True)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'product': self.product, 'form': self.form_class, 'commend': self.commend})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.product = self.product
            data.save()
        return redirect('pages:product_detail', self.product.slug)
