from django.db.models import Q
from django.shortcuts import render, reverse, resolve_url, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Category
from products.models import Products
from django.shortcuts import get_object_or_404
from products.forms import CommendForm, CommendReplyForm
from products.models import Commend, Brand
from django.contrib.auth.decorators import login_required
from .froms import SearchForm, FilterForm


class HomeView(View):
    template_name = 'pages/index.html'
    form_class = SearchForm
    form_class_2 = FilterForm

    def get(self, request, slug_category=None, brand_slug=None):
        categories = Category.objects.filter(is_sub_category=False)
        products = Products.objects.filter(is_active=True)
        brand = Brand.objects.all()

        if brand_slug:
            # for filter product with brand
            brand_s = Brand.objects.get(slug=brand_slug)
            products = Products.objects.filter(is_active=True, brand=brand_s)
        if slug_category:
            # for show information product
            category = Category.objects.filter(slug=slug_category)
            products = Products.objects.filter(Q(category__in=category))
        if request.GET.get('search'):
            # search in product
            products = products.filter(title__contains=request.GET['search'])

        if request.GET.get('filter_min') and request.GET.get('filter_max'):
            # for filter product with min price and max price
            products = products.filter(price__range=(request.GET.get('filter_min'), request.GET.get('filter_max')))
        if request.GET.get('filter_min'):
            # filter product with min price
            filter = []
            for item in products:
                filter.append(item.price)
            m = max(filter)
            products = products.filter(price__range=(request.GET.get('filter_min'), m))
        if request.GET.get('filter_max'):
            # filter product with min price
            filter = []
            for item in products:
                filter.append(item.price)
            m = min(filter)
            products = products.filter(price__range=(m, request.GET.get('filter_max')))
        #     -------------
        return render(request, self.template_name,
                      {'products': products, 'categories': categories, 'form_search': self.form_class,
                       'filter': self.form_class_2, 'brand': brand})


class ProductsDetailView(View):
    template_name = 'pages/detail.html'
    form_class = CommendForm
    form_reply_class = CommendReplyForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Products, slug=kwargs['slug'])
        self.commends = Commend.objects.filter(active=True, is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'product': self.product, 'form': self.form_class, 'commends': self.commends,
                   'form_reply': self.form_reply_class, }

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
