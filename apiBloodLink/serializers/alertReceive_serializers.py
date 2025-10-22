from rest_framework import serializers
from ..models.alertReceive_models import AlerteReceive
from ..models.provider_models import Provider
from ..models.alert_models import Alert

class AlertReceiveSerializers(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only = True)
    alert_id = serializers.CharField(source='alert.id', read_only = True)
    
    class Meta:
        model = AlerteReceive
        fields = '__all__'
        read_only_fields = ['id', 'date']