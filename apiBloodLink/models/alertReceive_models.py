from django.db import models
from .provider_models import Provider
from .alert_models import Alert
import uuid

class AlerteReceive(models.Model):
    """Alerte envoyée entre fournisseur et banque de sang"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    models.DateTimeField(auto_now_add=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='alerts')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='alerts')

    def __str__(self):
        return f"Alerte {self.date} - {self.provider.name} → {self.bank.name}"
