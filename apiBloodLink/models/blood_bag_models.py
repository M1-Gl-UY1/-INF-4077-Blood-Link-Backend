from django.db import models
import uuid

class BloodBag(models.Model):
    """Représente une poche de sang donnée ou reçue"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    blood_group = models.CharField(max_length=1)
    rhesus = models.CharField(max_length=1)

    def __str__(self):
        return f"Poche {self.blood_group}{self.rhesus}"
