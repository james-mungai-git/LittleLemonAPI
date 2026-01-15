from django.urls import path
from .views import MenuItemViewSet
 
urlpatterns = [
    path('menuitems/', MenuItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='menuitem-list'),

    path('menuitems/<int:pk>/', MenuItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='menuitem-detail'),
]