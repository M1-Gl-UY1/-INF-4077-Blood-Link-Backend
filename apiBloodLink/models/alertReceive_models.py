from django.db import models
from .provider_models import Provider
from .alert_models import Alert
import uuid

class AlerteReceive(models.Model):
    """Alerte envoyée entre fournisseur et banque de sang"""
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('SENT', 'Envoyée'),
        ('RECEIVED', 'Reçue'),
        ('IN_PROGRESS', 'En cours de traitement'),
        ('RESOLVED', 'Résolue'),
        ('CANCELLED', 'Annulée'),
        ('FAILED', 'Échouée'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS_CHOICES)
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='alerts')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='alerts')

    def __str__(self):
        return f"Alerte {self.date}"
