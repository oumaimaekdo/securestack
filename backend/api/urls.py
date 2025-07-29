from django.urls import path
from . import views
from .views import (
    RegisterView, secured_view, admin_only_view, promote_to_admin,
    ServerListCreateView, ServerRetrieveUpdateDestroyView,
    BackupTaskListCreateView, BackupTaskRetrieveUpdateDestroyView,
    IncidentListCreateView, IncidentRetrieveUpdateDestroyView,
    limited_view
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Auth & sécurité
    path('register/', RegisterView.as_view(), name='register'),
    path('secured/', secured_view, name='secured_view'),
    path('admin-only/', admin_only_view, name='admin_only_view'),
    path('promote-admin/', promote_to_admin, name='promote_to_admin'),
    path('promote/', promote_to_admin, name='promote-to-admin'),
    path('limited/', limited_view, name='limited_view'),

    # Serveurs
    path('servers/', ServerListCreateView.as_view(), name='server-list-create'),
    path('servers/<int:pk>/', ServerRetrieveUpdateDestroyView.as_view(), name='server-detail'),

    # Backups
    path('backups/', BackupTaskListCreateView.as_view(), name='backup-list-create'),
    path('backups/<int:pk>/', BackupTaskRetrieveUpdateDestroyView.as_view(), name='backup-detail'),


    # Incidents
    path('incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('incidents/<int:pk>/', IncidentRetrieveUpdateDestroyView.as_view(), name='incident-detail'),
    

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Tests
    path('test/', views.test_api),

    # Statut 
    path('status/', views.status_check, name='status_check'), 
]
