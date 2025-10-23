from django.db import models
import uuid
from .provider_models import Provider
from .blood_bag_models import BloodBag
from django.contrib.auth.hashers import make_password


class BloodBank(models.Model):
    """ Banque de sang """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=127)
    email = models.EmailField(max_length=127, unique=True)
    
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # Relation avec la poche de sang
    blood_bags = models.ManyToManyField('BloodBag', through='BloodTransaction', related_name='banks' )
    
    
    def save(self, *args, **kwargs):
        # Hachage automatique du mot de passe avant enregistrement
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class BloodTransaction(models.Model):
    """ Don de sang entre une banque de sang et un fournisseur """

    # TRANSACTION_TYPE = [
    #     ('give', 'Donner'),
    #     ('receive', 'Recevoir')
    # ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='transactions'  # Toutes les transactions faites par un fournisseur
    )
    bank = models.ForeignKey(
        BloodBank,
        on_delete=models.CASCADE,
        related_name='transactions'  # Toutes les transactions associées à une banque
    )
    blood_bag = models.ForeignKey(
        BloodBag,
        on_delete=models.CASCADE,
        related_name='transactions'  # Historique des transactions liées à un sac de sang
    )
    # transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"- {self.blood_bag} - {self.date}"
