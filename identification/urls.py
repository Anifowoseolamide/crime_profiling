from django.urls import path
from .views import IdentifyView, IdentificationLogListView

urlpatterns = [
    path('', IdentifyView.as_view(), name='identify'),
    path('logs/', IdentificationLogListView.as_view(), name='identification-logs'),
]
