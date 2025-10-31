# apiBloodLink/serializers/doctor_serializers.py
from re import U
from rest_framework import serializers
from ..models.doctor_models import Doctor, BloodRequest
from ..models.blood_bank_models import BloodBank
from ..serializers.user_serializers import UserSerializer

class BloodRequestSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='docteur.name', read_only=True)
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodRequest
        fields = "__all__"
        read_only_fields = ["id", "date_request"]


class DoctorSerializer(serializers.ModelSerializer):
    blood_requests = BloodRequestSerializer(source='bloodrequest_set', many=True, read_only=True)
    bank_id = serializers.CharField(source='blood_bank.id', read_only=True )
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ["id"]
        
