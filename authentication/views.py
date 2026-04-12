from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash

from .models import Officer, PoliceStation
from .serializers import (
    LagoscpTokenObtainPairSerializer,
    OfficerSerializer,
    OfficerCreateSerializer,
    OfficerMiniSerializer,
    PoliceStationSerializer,
    ChangePasswordSerializer,
)
from audit.mixins import AuditLogMixin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsSupervisorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('SUPERVISOR', 'ADMIN')


class OfficerLoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Body: { "badge_number": "LSP-04821", "password": "..." }
    Returns: access + refresh tokens + officer profile
    """
    serializer_class = LagoscpTokenObtainPairSerializer


class OfficerTokenRefreshView(TokenRefreshView):
    """POST /api/auth/refresh/"""
    pass


class OfficerLogoutView(APIView):
    """POST /api/auth/logout/ — blacklist the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class OfficerMeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me/ — authenticated officer's own profile."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OfficerSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """POST /api/auth/change-password/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        officer = request.user
        if not officer.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        officer.set_password(serializer.validated_data['new_password'])
        officer.save()
        return Response({'detail': 'Password updated.'}, status=status.HTTP_200_OK)


class OfficerListCreateView(AuditLogMixin, generics.ListCreateAPIView):
    """
    GET  /api/auth/officers/   — list all officers (Admin/Supervisor)
    POST /api/auth/officers/   — create new officer (Admin only)
    """
    queryset = Officer.objects.select_related('station').order_by('badge_number')
    audit_action = 'OFFICER_CREATED'
    audit_target_type = 'Officer'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfficerCreateSerializer
        return OfficerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsSupervisorOrAdmin()]


class OfficerDetailView(AuditLogMixin, generics.RetrieveUpdateAPIView):
    """
    GET   /api/auth/officers/{id}/
    PATCH /api/auth/officers/{id}/
    """
    queryset = Officer.objects.select_related('station')
    serializer_class = OfficerSerializer
    permission_classes = [IsSupervisorOrAdmin]
    audit_action = 'OFFICER_UPDATED'
    audit_target_type = 'Officer'


class PoliceStationListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/auth/stations/
    POST /api/auth/stations/ (Admin only)
    """
    queryset = PoliceStation.objects.all().order_by('name')
    serializer_class = PoliceStationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class PoliceStationDetailView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/stations/{id}/"""
    queryset = PoliceStation.objects.all()
    serializer_class = PoliceStationSerializer
    permission_classes = [IsAdmin]
