from django.urls import path
from .views import (
    ReservView,
    AddReservItemView,
    DeleteReservItemView,

    OrderConfirmationView,
    AddOrderView,
    ListOrderView,
    OrderDetailView
)

app_name = 'orders'

urlpatterns = [
    path('reserv/', ReservView.as_view(), name='reserv'),
    path('reserv/add_item/<int:pk>/', AddReservItemView.as_view(), name='add_reserv_item'),
    path('reserv/delete_item/<int:pk>/', DeleteReservItemView.as_view(), name='delete_reserv_item'),
    path('order/order_confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('order/add_order/', AddOrderView.as_view(), name='add_order'),
    path('orders/', ListOrderView.as_view(), name='orders'),
    path('orders/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail')
]
