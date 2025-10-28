# apiBloodLink/serializers/provider_serializers.py
from rest_framework import serializers
from ..models.provider_models import Provider
from ..serializers.user_serializers import UserSerializer

class ProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Provider
        fields = '__all__'
        read_only_fields = ["id"]
