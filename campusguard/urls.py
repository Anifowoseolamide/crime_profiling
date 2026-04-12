"""
URL configuration for LagosCP — Lagos State Crime Profiling System.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Authentication (officer login / token management)
    path('api/auth/', include('authentication.urls')),

    # Core LagosCP modules
    path('api/subjects/', include('subjects.urls')),
    path('api/offences/', include('offences.urls')),
    path('api/identify/', include('identification.urls')),
    path('api/wanted/', include('wanted.urls')),
    path('api/audit/', include('audit.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
