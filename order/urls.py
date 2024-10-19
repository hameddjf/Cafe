from django.urls import path

from .views import OrderListCreateView

app_name = 'qr_login'

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list'),
]
