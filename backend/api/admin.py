from django.contrib import admin
from .models import Server, BackupTask, Incident

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'operating_system', 'created_by', 'created_at')
    search_fields = ('name', 'ip_address')
    list_filter = ('operating_system', 'created_by')

@admin.register(BackupTask)
class BackupTaskAdmin(admin.ModelAdmin):
    list_display = ('server', 'date', 'status')
    search_fields = ('server__name',)
    list_filter = ('status',)

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('server', 'title', 'detected_at', 'resolved')
    search_fields = ('title', 'server__name')
    list_filter = ('resolved',)
