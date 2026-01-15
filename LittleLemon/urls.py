from django.urls import path
from .views import (
   
    cart,
    OrderViewSet,
)

urlpatterns = [
    path('cart/', cart, name='cart'),
                                
     path('orders/', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='orders-list'),

    path('orders/<int:pk>/', OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='orders-detail'),
]