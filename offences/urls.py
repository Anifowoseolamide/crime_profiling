from django.urls import path
from .views import OffenceListView, OffenceDetailView, CrimeHotspotView

urlpatterns = [
    path('', OffenceListView.as_view(), name='offence-list'),
    path('hotspots/', CrimeHotspotView.as_view(), name='offence-hotspots'),
    path('<uuid:pk>/', OffenceDetailView.as_view(), name='offence-detail'),
]
