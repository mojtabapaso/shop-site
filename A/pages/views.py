from django.db.models import Q
from django.shortcuts import render, reverse, resolve_url, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category
from products.models import Brand, Products
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from products.forms import CommendForm, CommendReplyForm
from products.models import Commend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class HomeView(View):
    template_name = 'pages/index.html'

    def get(self, request, slug_category=None):
        categories = Category.objects.filter(is_sub_category=False)
        products = Products.objects.all()
        if slug_category:
            category = Category.objects.filter(slug=slug_category)
            products = Products.objects.filter(Q(category__in=category))
        return render(request, 'pages/index.html', {'products': products, 'categories': categories})


class ProductsDetailView(View):
    #
    template_name = 'pages/detail.html'
    form_class = CommendForm
    form_reply_class = CommendReplyForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Products, slug=kwargs['slug'])
        self.commends = Commend.objects.filter(active=True, is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'product': self.product, 'form': self.form_class, 'commends': self.commends,
                   'form_reply': self.form_reply_class}
        return render(request, self.template_name, context=context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.product = self.product
            data.save()
        return redirect('pages:product_detail', self.product.slug)


class AddCommendView(View):
    form_class = CommendReplyForm

    # save commend whit ID product and ID commend
    def post(self, request, product_id, commend_id):
        product = get_object_or_404(Products, pk=product_id)
        commend = get_object_or_404(Commend, pk=commend_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.product = product
            data.reply = commend
            data.is_reply = True
            data.save()
        return redirect('pages:product_detail', product.slug)
