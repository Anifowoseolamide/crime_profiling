from django.urls import path
from .views import WantedListView, WantedDetailView

urlpatterns = [
    path('', WantedListView.as_view(), name='wanted-list'),
    path('<uuid:pk>/', WantedDetailView.as_view(), name='wanted-detail'),
]
