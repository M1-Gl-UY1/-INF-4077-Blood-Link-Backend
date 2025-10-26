from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction

from ..models.blood_bank_models import  *
from ..models.blood_bag_models import BloodBag
from ..models.provider_models import Provider



@transaction.atomic
def TransactionCreateView(provider_id, bank_id):
    try:
        provider = Provider.objects.get(id=provider_id)
        bank = BloodBank.objects.get(id=bank_id)
    
        providerInstance  = Provider.objects.get(id=provider_id)
        bloodbag = BloodBag.objects.create(
            blood_group=providerInstance.blood_group,  # tu peux adapter selon ton modèle Provider
            rhesus=providerInstance.rhesus,
            provider=providerInstance
        )
    
        transaction = BloodTransaction.objects.create(
            provider_id=provider_id,
            bank_id=bank_id,
            blood_bag=bloodbag
        )
        return transaction
    
    except (Provider.DoesNotExist, BloodBank.DoesNotExist):
        return None
    