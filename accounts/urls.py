from django.urls import path
from .views import (
    RegisterView,
    LoginView,
   
   
)
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  
    path('groups/managers/users/',views.groups),
    path('groups/list-managers/users/',views.list_managers),
    path('groups/list-managers/users/<int:pk>/',views.list_managers),
    path('groups/list_delivery_crew/users/',views.list_delivery_crew), 
    path('groups/list_delivery_crew/users/<int:pk>/',views.list_delivery_crew), 
    path('auth-token/', obtain_auth_token), 
    path('home/', views.home, name='home'),  
    path('register/', views.login, name='register-user'), 
]