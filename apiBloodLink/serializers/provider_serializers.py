# apiBloodLink/serializers/provider_serializers.py
from rest_framework import serializers
from ..models.provider_models import Provider

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'sexe',
            'email',
            'phone_number',
            'blood_group',
            'rhesus',
            'last_give',
            'historique_medical'
        ]
        read_only_fields = ["id"]
