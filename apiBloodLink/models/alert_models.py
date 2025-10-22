from django.db import models
from .provider_models import Provider
from .blood_bank_models import BloodBank
from .blood_bank_models import *
import uuid

class Alert(models.Model):
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
    creates_date = models.DateField()
    Resolved_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name = 'emit')
    
    

    def __str__(self):
        return f"Alerte {self.id} - {self.status}"
