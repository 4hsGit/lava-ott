from django.urls import path
from .views import *

urlpatterns = [
    # Test
    path('checkout-test/', PaymentCheckoutTestView.as_view(), name='checkout-test'),
    # Live
    path('checkout/', PaymentCheckoutView.as_view(), name='checkout-test'),

    path('response/', PaymentResponseView.as_view(), name='response-test'),
]
