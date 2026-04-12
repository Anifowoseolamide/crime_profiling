from django.urls import path
from .views import (
    OfficerLoginView,
    OfficerTokenRefreshView,
    OfficerLogoutView,
    OfficerMeView,
    ChangePasswordView,
    OfficerListCreateView,
    OfficerDetailView,
    PoliceStationListCreateView,
    PoliceStationDetailView,
)

urlpatterns = [
    # Auth
    path('login/', OfficerLoginView.as_view(), name='officer-login'),
    path('refresh/', OfficerTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', OfficerLogoutView.as_view(), name='officer-logout'),
    path('me/', OfficerMeView.as_view(), name='officer-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Officer management (Admin)
    path('officers/', OfficerListCreateView.as_view(), name='officer-list'),
    path('officers/<uuid:pk>/', OfficerDetailView.as_view(), name='officer-detail'),

    # Station management
    path('stations/', PoliceStationListCreateView.as_view(), name='station-list'),
    path('stations/<uuid:pk>/', PoliceStationDetailView.as_view(), name='station-detail'),
]
