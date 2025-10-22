from django.db import models
import uuid
from .blood_bank_models import BloodBank

from django.contrib.auth.hashers import make_password

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
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hachage automatique du mot de passe avant enregistrement
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.name} ({self.get_grade_display()} - {self.get_speciality_display()})"


""" Requete envoye par le Docteur  a une banque"""

class BloodRequest(models.Model):
    
    BloodRequest_status =[
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        
    ]

    docteur = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='blood_requests')
    date_request =  models.DateTimeField(auto_now_add=True)
    blood_group = models.CharField(max_length=1)
    rhesus = models.CharField(max_length=1)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=8, choices=BloodRequest_status, default='pending')
    
    