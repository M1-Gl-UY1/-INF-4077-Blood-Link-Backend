from django.shortcuts import render
from rest_framework import generics
from .models.doctor_models import Doctor
from .serializers.doctor_serializers import DoctorSerializer

from .models.blood_bank_models import *
from .serializers.blood_bank_serializers import *

from .models.blood_bag_models import BloodBag
from .serializers.blood_bag_serializers import BloodBagSerializer

from .models.alert_models import Alert
from .serializers.alert_Serializers import AlertSerializer


from .models.provider_models import *
from .serializers.provider_serializers import ProviderSerializer

from .models.alertReceive_models import AlerteReceive
from .serializers.alertReceive_serializers import AlertReceiveSerializers

# Create your views here.
# views for doctor
class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
class DoctorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = "id"
    
# views for blood-bank
class BloodBankListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer

class BloodBankRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    lookup_field = "id"

class BloodTransactionListCreateAPIView(generics.ListCreateAPIView):
    ueryset = BloodTransaction.objects.all()
    serializer_class = BloodTransactionSerializer

class BloodTransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    ueryset = BloodTransaction.objects.all()
    serializer_class = BloodTransactionSerializer
    lookup_field = "id"
    
# views for blood-bag

class BloodBagListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodBag.objects.all()
    serializer_class = BloodBagSerializer
    
class BloodBagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBag.objects.all()
    serializer_class = BloodBagSerializer
    lookup_field = "id"
    
# views for alert
class AlertListCreateAPIView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AlertRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    lookup_field = "id"


# views for Provider
class ProviderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProviderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    lookup_field = "id"

# views for Receive-

class AlerteReceiveListCreateAPIView(generics.ListCreateAPIView):
    queryset = AlerteReceive.objects.all()
    serializer_class = AlertReceiveSerializers

class AlerteReceiveRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlerteReceive.objects.all()
    serializer_class = AlertReceiveSerializers
    lookup_field = "id"
    
    
# views for bloodback

class BloodBagSerializerListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodBag.objects.all()
    
    
