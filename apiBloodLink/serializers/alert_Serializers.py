from rest_framework import serializers
from apiBloodLink.models.alert_models import Alert


class AlertSerializer(serializers.ModelSerializer):
    # Pour afficher le nom du provider et de la banque dans le serializer
    bank_name = serializers.CharField(source='bank.name', read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ["id","created_date"]
        # 'provider' et 'bank' gardent les IDs pour les relations
        # 'provider_name' et 'bank_name' affichent les noms lisibles
