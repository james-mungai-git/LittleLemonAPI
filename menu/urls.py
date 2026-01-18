from django.urls import path
from .views import MenuItemViewSet
 
urlpatterns = [
    path('menu-items/', MenuItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='menuitem-list'),

    path('menu-items/<int:pk>/', MenuItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='menuitem-detail'),
]