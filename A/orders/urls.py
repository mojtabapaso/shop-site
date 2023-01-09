from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.OrderView.as_view(), name='orders_view'),
    path('cart/', views.OrderSummaryView.as_view(), name='summary_cart'),
    path('apply/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('next/', views.LastStepView.as_view(), name='last_step'),
    path('add/<slug:product_slug>/', views.add_to_cart, name='add_cart'),
    path('remove/cart/<slug:product_slug>/', views.remove_from_cart, name='remove_cart'),
    path('remove/one/<slug:product_slug>/', views.remove_one_cart, name='remove_one_cart'),

]
