from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug_category>', views.HomeView.as_view(), name='category_slug'),
    path('<slug:slug>/', views.ProductsDetailView.as_view(), name='product_detail'),
]
