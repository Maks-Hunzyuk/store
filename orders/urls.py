from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView, OrderListView,
                          SuccessTemplateView, OrderDetailView)

app_name = "orders"


urlpatterns = [
    path("order_create/", OrderCreateView.as_view(), name='order_create'),
    path('order-success', SuccessTemplateView.as_view(), name='order_success'),
    path('order-cancel', CanceledTemplateView.as_view(), name='order_cancel'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order')
]
