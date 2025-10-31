from django.db import models
import uuid
from .blood_bank_models import BloodBank
from .user_models import User

from django.contrib.auth.hashers import make_password
from  django.contrib.auth.models  import AbstractUser

GRADE_CHOICES = [
    ('INT', 'Interne'),
    ('RES', 'Résident'),
    ('ASS', 'Assistant médical'),
    ('SPC', 'Spécialiste'),
    ('CHS', 'Chef de service'),
    ('PRF', 'Professeur'),
]

SPECIALITY_CHOICES = [
    ('GP', 'Généraliste'),
    ('CD', 'Cardiologue'),
    ('NE', 'Neurologue'),
    ('OR', 'Orthopédiste'),
    ('PD', 'Pédiatre'),
]

class Doctor(models.Model):
    """Informations sur un médecin"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=4, choices=GRADE_CHOICES, default='INT')
    speciality = models.CharField(max_length=2, choices=SPECIALITY_CHOICES, default='GP')
    # password = models.CharField(max_length=255)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='linked', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     # Hachage automatique du mot de passe avant enregistrement
    #     if not self.password.startswith('pbkdf2_'):
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.name} ({self.grade} - {self.speciality})"


""" Requete envoye par le Docteur  a une banque"""

class BloodRequest(models.Model):
    
    BloodRequest_status =[
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        
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
    date_request =  models.DateTimeField(auto_now_add=True)
    
    docteur = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='blood_requests')
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='blood_requests', null=True, blank=True)
    
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=3)
    rhesus = models.CharField(choices=RHESUS_CHOICES, max_length=3)
    
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=8, choices=BloodRequest_status, default='pending')
    
    