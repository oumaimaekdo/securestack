
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Server, BackupTask, Incident

class RegisterSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True  # active le compte
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'date_joined']

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


class BackupTaskSerializer(serializers.ModelSerializer):
    server_name = serializers.ReadOnlyField(source='server.name')

    class Meta:
        model = BackupTask
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    server_name = serializers.ReadOnlyField(source='server.name')

    class Meta:
        model = Incident
        fields = '__all__'
