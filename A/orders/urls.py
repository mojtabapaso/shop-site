from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.OrderView.as_view(),name='orders_view')
]
