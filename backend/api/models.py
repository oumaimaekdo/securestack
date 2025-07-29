from django.db import models
from django.contrib.auth.models import User

class Server(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class BackupTask(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='backups')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Backup on {self.server.name} at {self.date}"


class Incident(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='incidents')
    title = models.CharField(max_length=100)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {'Resolved' if self.resolved else 'Open'}"
