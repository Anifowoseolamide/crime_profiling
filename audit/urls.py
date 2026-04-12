from django.urls import path
from .views import AuditLogListView, AuditLogExportView, AuditLogFeedView, DashboardStatsView

urlpatterns = [
    path('', AuditLogListView.as_view(), name='audit-log-list'),
    path('feed/', AuditLogFeedView.as_view(), name='audit-log-feed'),
    path('stats/', DashboardStatsView.as_view(), name='audit-stats'),
    path('export/', AuditLogExportView.as_view(), name='audit-log-export'),
]
