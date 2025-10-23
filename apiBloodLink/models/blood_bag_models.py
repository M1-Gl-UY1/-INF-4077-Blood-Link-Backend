from django.db import models
import uuid

from django.forms import model_to_dict

class BloodBag(models.Model):
    """Représente une poche de sang donnée ou reçue"""
    
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
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES)
    rhesus = models.CharField(choices=RHESUS_CHOICES)

    def __str__(self):
        return f"Poche {self.blood_group}{self.rhesus}"
