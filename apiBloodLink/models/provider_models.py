from django.db import models
import uuid
from django.contrib.auth.hashers import make_password


class Provider(models.Model):
    
    "Donneur de sang ou fournisseur"
    
    SEX_CHOICES=[
        ('M', 'Masculin'),('F', 'Féminin')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False  )
    name = models.CharField(max_length=50)
    sexe = models.CharField(choices=SEX_CHOICES, default='M')
    date_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=127, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    blood_group = models.CharField(max_length=1)
    rhesus = models.CharField(max_length=1)
    last_give = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=255)
    historique_medical = models.FileField(upload_to='medical_histories/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.blood_group}{self.rhesus})"
    
    def save(self, *args, **kwargs):
        # Hachage automatique du mot de passe avant enregistrement
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

   