from django.db import models
from .provider_models import Provider
from .alert_models import Alert
import uuid

class AlerteReceive(models.Model):
    """Alerte envoyée entre fournisseur et banque de sang"""
    
    STATUS_CHOICES = [
    ('PENDING', 'En attente de réponse'),   # LE PROVIDER n’a pas encore répondu
    ('RESPONDED', 'Répondue'),              # LE PROVIDER a répondu (positive ou négative)
    ('COMPLETED', 'Terminée avec succès'),  # Sang livré ou besoin satisfait
    ('CANCELLED', 'Annulée'),               # Alerte annulée par la banque ou le fournisseur
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS_CHOICES,  max_length=20, default='PENDING')
     
     # liaison avec le provider qui recoit une alerte
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='alerts')

    class Meta:
        unique_together = ('alert', 'provider')
        
    def __str__(self):
        return f"Reply({self.provider.name} → Alerte {self.alert.id})"
