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
    
    RHESUS_CHOICES = [
        ('POS', '+'),
        ('NEG', '-'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_date = models.DateField()
    Resolved_date = models.DateField()
    blood_groupe = models.CharField(choices=BLOOD_GROUP_CHOICES)
    rhesus = models.CharField(choices=RHESUS_CHOICES)
    
    # liaison avec la banque qui emmet une alerte
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name = 'emitted_alerts')
    
    

    def __str__(self):
        return f"Alerte {self.id} - {self.status}"
