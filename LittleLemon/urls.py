from django.urls import path,include
from .views import (
   
    cart,
    OrderViewSet,
)
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(r"cart/orders",OrderViewSet,basename='orders')

urlpatterns = [
    path('cart/menu-items/', cart, name='cart'),
    path('',include(router.urls))
]