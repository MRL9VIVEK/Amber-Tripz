from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('checkout/<slug:slug>', views.CHECKOUT, name="checkout"),
    path('verify_payment', views.VERIFY_PAYMENT, name="verify_payment"),
]