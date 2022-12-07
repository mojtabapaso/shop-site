from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Category
from products.models import Brand, Laptop


class HomeView(TemplateView):
    template_name = 'pages/index.html'


class DetailProductView(View):
    pass
