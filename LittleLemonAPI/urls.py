from django.contrib import admin
from django.urls import path,include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('api/',include('LittleLemon.urls')),
    path('api/',include('accounts.urls')),
    path('api/',include('menu.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
