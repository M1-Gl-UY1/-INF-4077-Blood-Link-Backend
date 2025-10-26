from ..models.alert_models import *
from ..models.doctor_models import *
from ..models.alertReceive_models import AlerteReceive
from django.db import transaction

@transaction.atomic
def validate_request_and_create_alert(request_id):
    
    try:
        blood_request = BloodRequest.objects.select_for_update().get(id=request_id)

        if blood_request.status != 'pending':
            return None
        
        #validation d'une requette
        blood_request.status = 'approved'
        blood_request.save()
        
        # creation automatique de l'alerte
        
        alert = Alert.objects.create(
            bank = blood_request.bank,
            blood_groupe = blood_request.blood_group,
            rhesus = blood_request.rhesus,
            status = 'PENDING'
        )
        return alert
    
    except BloodRequest.DoesNotExist:
        return None