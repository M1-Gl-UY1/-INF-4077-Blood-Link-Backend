import email
from django.shortcuts import render
from rest_framework import generics
from .models.doctor_models import *
from .serializers.doctor_serializers import *
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from .models.blood_bank_models import *
from .serializers.blood_bank_serializers import * # type: ignore

from .models.blood_bag_models import BloodBag
from .serializers.blood_bag_serializers import BloodBagSerializer

from .models.alert_models import Alert
from .serializers.alert_Serializers import AlertSerializer


from .models.provider_models import *
from .serializers.provider_serializers import ProviderSerializer

from .models.alertReceive_models import AlerteReceive
from .serializers.alertReceive_serializers import AlertReceiveSerializers

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers.user_serializers import UserSerializer
from .serializers.LoginSerializer import LoginSerializer # type: ignore

from .models.user_models import User

import jwt, datetime

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
    queryset = BloodTransaction.objects.all()
    serializer_class = BloodTransactionSerializer

class BloodTransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodTransaction.objects.all()
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
    
    
# views for bloodbag

# class BloodBagListCreateAPIView(generics.ListCreateAPIView):
#     queryset = BloodBag.objects.all()
#     serializer_class = BloodBagSerializer
    
# class BloodBagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BloodBag.objects.all()
#     serializer_class = BloodBagSerializer
#     lookup_field = "id"


class BloodRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    
class BloodRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    lookup_field = "id"


# ajout des vue login et register dans views.py
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginAPIView(APIView):
    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # # Appel de create() pour générer le token
        # data = serializer.create(serializer.validated_data)
        # return Response(data, status=status.HTTP_200_OK)
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': str(user.id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        
        return response
                     
                
class UserViews(APIView):
    def get(self, request):
        
        data = request.data
        token = data.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response