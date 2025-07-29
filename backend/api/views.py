from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

import logging

from .serializers import (
    RegisterSerializer, UserListSerializer,
    ServerSerializer, BackupTaskSerializer, IncidentSerializer
)
from .models import Server, BackupTask, Incident

logger = logging.getLogger(__name__)

# ----------- Auth & Admin Views -----------

@method_decorator(ratelimit(key='ip', rate='3/m', block=True), name='post')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secured_view(request):
    logger.info(f"{request.user.username} a accédé à /api/secured/")
    return Response({"message": "Données sécurisées accessibles."})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_only_view(request):
    return Response({"message": "Bienvenue admin ! Vous avez accès à cette vue protégée."})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def promote_to_admin(request):
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)

        if user.is_staff:
            logger.info(f"{request.user.username} a tenté de promouvoir {username}, qui est déjà admin.")
            return Response({"message": f"{username} est déjà admin."}, status=status.HTTP_200_OK)

        user.is_staff = True
        user.save()
        logger.info(f"{request.user.username} a promu {username} en admin.")
        return Response({"message": f"{username} est maintenant admin."})
    except User.DoesNotExist:
        logger.warning(f"{request.user.username} a tenté de promouvoir un utilisateur inexistant : {username}.")
        return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def test_api(request):
    return Response({"message": "API opérationnelle ! 🔐"})
    

# ----------- ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def limited_view(request):
    return JsonResponse({'message': 'Bienvenue, tu n’as pas dépassé la limite 🚀'})

# ----------- CRUD Views for Server, BackupTask, Incident -----------

class ServerListCreateView(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        logger.info(f"{self.request.user.username} a créé le serveur '{instance.name}' ({instance.ip_address}).")

class ServerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        logger.warning(f"{self.request.user.username} a supprimé le serveur '{instance.name}' ({instance.ip_address}).")
        super().perform_destroy(instance)


class BackupTaskListCreateView(generics.ListCreateAPIView):
    queryset = BackupTask.objects.all()
    serializer_class = BackupTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"{self.request.user.username} a créé une tâche de backup pour le serveur ID {instance.server.id} à {instance.date}.")

class BackupTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BackupTask.objects.all()
    serializer_class = BackupTaskSerializer   

    def perform_destroy(self, instance):
        logger.warning(f"{self.request.user.username} a supprimé une tâche de backup du {instance.date} pour le serveur ID {instance.server.id}.")
        super().perform_destroy(instance)     

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"{self.request.user.username} a signalé un incident '{instance.title}' sur le serveur ID {instance.server.id} à {instance.detected_at}.")    

class IncidentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        logger.warning(f"{self.request.user.username} a supprimé l'incident '{instance.title}' sur le serveur ID {instance.server.id}.")
        super().perform_destroy(instance)


@api_view(['GET'])
def status_check(request):
    return Response({"status": "API opérationnelle ✅"})

