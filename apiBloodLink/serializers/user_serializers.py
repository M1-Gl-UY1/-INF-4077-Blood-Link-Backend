from re import U
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models.doctor_models import Doctor
from ..models.provider_models import Provider
from ..models.blood_bank_models import BloodBank

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
    
        #creation des profils associés en fonction du rôle
        if user.role == 'doctor': # type: ignore
            Doctor.objects.create(user=user)
        elif user.role == 'provider': # type: ignore
            Provider.objects.create(user=user)
        elif user.role == 'bank': # type: ignore
            BloodBank.objects.create(user=user)  
        return user