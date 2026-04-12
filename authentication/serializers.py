from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Officer, PoliceStation


class PoliceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStation
        fields = ['id', 'name', 'division', 'lga', 'address', 'phone']


class OfficerMiniSerializer(serializers.ModelSerializer):
    """Compact officer info for nested use (e.g. in offence records)."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    station_name = serializers.CharField(read_only=True)

    class Meta:
        model = Officer
        fields = ['id', 'badge_number', 'full_name', 'rank', 'role', 'station_name']


class OfficerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    station = PoliceStationSerializer(read_only=True)
    station_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Officer
        fields = [
            'id', 'badge_number', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'rank', 'role', 'station', 'station_id',
            'is_active', 'last_login', 'created_at',
        ]
        read_only_fields = ['id', 'last_login', 'created_at']

    def update(self, instance, validated_data):
        station_id = validated_data.pop('station_id', None)
        if station_id is not None:
            try:
                instance.station = PoliceStation.objects.get(id=station_id)
            except PoliceStation.DoesNotExist:
                raise serializers.ValidationError({'station_id': 'Station not found.'})
        return super().update(instance, validated_data)


class OfficerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    station_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Officer
        fields = [
            'badge_number', 'first_name', 'last_name', 'email', 'phone',
            'rank', 'role', 'station_id', 'password',
        ]

    def create(self, validated_data):
        station_id = validated_data.pop('station_id', None)
        password = validated_data.pop('password')
        officer = Officer(**validated_data)
        officer.set_password(password)
        if station_id:
            try:
                officer.station = PoliceStation.objects.get(id=station_id)
            except PoliceStation.DoesNotExist:
                raise serializers.ValidationError({'station_id': 'Station not found.'})
        officer.save()
        return officer


class LagoscpTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT claim: embed officer details so the frontend doesn't need
    a separate /me/ request on initial login.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['badge_number'] = user.badge_number
        token['full_name'] = user.get_full_name()
        token['rank'] = user.rank
        token['role'] = user.role
        token['station'] = user.station_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        officer = self.user
        data['officer'] = {
            'id': str(officer.id),
            'badge_number': officer.badge_number,
            'full_name': officer.get_full_name(),
            'rank': officer.rank,
            'role': officer.role,
            'station': officer.station_name,
        }
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
