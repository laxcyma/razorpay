from django.urls import path, include
from razorapi import views
urlpatterns = [
    path('',views.payment_panel, name='payment_panel'),
    path('payment_status/',views.payment_status, name='payment_status'),
]
