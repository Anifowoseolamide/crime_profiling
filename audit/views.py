import csv
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer


class IsSupervisorAnalystOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('SUPERVISOR', 'ANALYST', 'ADMIN')


class AuditLogListView(generics.ListAPIView):
    """
    GET /api/audit/
    Query params: officer_id, action, target_type, start, end
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsSupervisorAnalystOrAdmin]

    def get_queryset(self):
        qs = AuditLog.objects.select_related('officer').order_by('-timestamp')
        params = self.request.query_params

        if officer_id := params.get('officer_id'):
            qs = qs.filter(officer__id=officer_id)
        if action := params.get('action'):
            qs = qs.filter(action__icontains=action)
        if target_type := params.get('target_type'):
            qs = qs.filter(target_type=target_type)
        if start := params.get('start'):
            qs = qs.filter(timestamp__date__gte=start)
        if end := params.get('end'):
            qs = qs.filter(timestamp__date__lte=end)

        return qs


class AuditLogExportView(APIView):
    """
    GET /api/audit/export/?... — download audit log as CSV
    """
    permission_classes = [IsSupervisorAnalystOrAdmin]

    def get(self, request):
        qs = AuditLog.objects.select_related('officer').order_by('-timestamp')
        params = request.query_params

        if officer_id := params.get('officer_id'):
            qs = qs.filter(officer__id=officer_id)
        if start := params.get('start'):
            qs = qs.filter(timestamp__date__gte=start)
        if end := params.get('end'):
            qs = qs.filter(timestamp__date__lte=end)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="audit_log.csv"'

        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Officer', 'Badge', 'Action', 'Target Type', 'Target ID', 'IP Address'])
        for log in qs:
            officer_name = log.officer.get_full_name() if log.officer else 'SYSTEM'
            badge = log.officer.badge_number if log.officer else '-'
            writer.writerow([
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                officer_name, badge,
                log.action, log.target_type,
                str(log.target_id) if log.target_id else '',
                log.ip_address or '',
            ])

        return response

class AuditLogFeedView(APIView):
    """
    GET /api/audit/feed/
    Returns a unified, formatted activity feed for the dashboard.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = AuditLog.objects.select_related('officer').order_by('-timestamp')[:50]
        
        feed = []
        for log in qs:
            officer_name = f"{log.officer.rank} {log.officer.get_full_name()}" if log.officer else "SYSTEM"
            
            action_map = {
                'SUBJECT_IDENTIFIED': ('SCAN', 'Completed field scan — MATCH FOUND'),
                'FAILED_IDENTIFICATION': ('SCAN', 'Completed field scan — NO MATCH'),
                'OFFENCE_CREATED': ('OFFENCE', 'Logged new offence'),
                'SUBJECT_VIEWED': ('VIEW', 'Viewed profile'),
                'MUGSHOT_ENROLLED': ('VIEW', 'Enrolled new mugshot'),
            }
            
            log_type, display_action = action_map.get(
                log.action, 
                ('VIEW', f"{log.action}")
            )
            # handle warrant action names that might be generated
            if 'WANTED' in log.action or 'WARRANT' in log.action:
                log_type, display_action = ('WARRANT', 'Issued warrant')

            subject_id_display = str(log.target_id)[0:8] if log.target_id else 'N/A'

            feed.append({
                'id': str(log.id),
                'time': log.timestamp.strftime('%H:%M:%S'),
                'officer': officer_name,
                'action': display_action,
                'subject': f"ID-{subject_id_display.upper()}",
                'type': log_type
            })

        return Response(feed)

class DashboardStatsView(APIView):
    """
    GET /api/audit/stats/
    Returns real-time dashboard metrics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from subjects.models import Subject
        from offences.models import Offence
        from identification.models import IdentificationLog
        from wanted.models import WantedPerson
        from django.utils import timezone
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        stats = {
            'total_subjects': Subject.objects.count(),
            'active_cases': Offence.objects.exclude(status__in=['RESOLVED', 'ACQUITTED', 'DISMISSED']).count(),
            'alerts_today': WantedPerson.objects.filter(created_at__gte=today_start).count(),
            'scans_today': IdentificationLog.objects.filter(timestamp__gte=today_start).count(),
        }
        
        return Response(stats)
