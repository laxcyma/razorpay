from django.urls import path
from . import razorpay

urlpatterns = [
    path('config/',views.payment_panel, name='payment_panel'),
    path('payment_status/',views.payment_status, name='payment_status'),
]
