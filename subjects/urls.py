from django.urls import path
from .views import (
    SubjectListView, 
    SubjectDetailView, 
    SubjectMugshotUploadView,
    SubjectTimelineView
)

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject-list'),
    path('<uuid:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('<uuid:pk>/timeline/', SubjectTimelineView.as_view(), name='subject-timeline'),
    path('<uuid:pk>/enrol-mugshot/', SubjectMugshotUploadView.as_view(), name='subject-enrol-mugshot'),
]
