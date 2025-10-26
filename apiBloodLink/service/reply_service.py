from django.db import transaction

from ..models.alertReceive_models import AlerteReceive
from ..models.alert_models import Alert
from ..models.provider_models import Provider


@transaction.atomic
def reply_to_alert(alert_id, provider_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        provider = Provider.objects.get(id=provider_id)
        
        
        #verifier si provider a deja repondu
        if AlerteReceive.objects.filter(alert=alert, provider=provider).exists():
            return None
        reply = AlerteReceive.objects.create(
            alert=alert,
            provider=provider,
            status='RESPONDED'
        )
        return reply
    
    except (Alert.DoesNotExist, Provider.DoesNotExist):
        return None