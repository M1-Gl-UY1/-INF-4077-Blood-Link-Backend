from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models.doctor_models import *
from .serializers.doctor_serializers import *

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

# ================================
#   DOCTOR
# ================================
class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
class DoctorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = "id"

# ================================
#   BLOOD BANK
# ================================
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

# ================================
#   BLOOD BAG
# ================================
class BloodBagListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodBag.objects.all()
    serializer_class = BloodBagSerializer
    
class BloodBagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBag.objects.all()
    serializer_class = BloodBagSerializer
    lookup_field = "id"

# ================================
#   ALERT
# ================================
class AlertListCreateAPIView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AlertRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    lookup_field = "id"

# ================================
#   PROVIDER
# ================================
class ProviderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProviderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    lookup_field = "id"

# ================================
#   ALERT RECEIVE
# ================================
class AlerteReceiveListCreateAPIView(generics.ListCreateAPIView):
    queryset = AlerteReceive.objects.all()
    serializer_class = AlertReceiveSerializers

class AlerteReceiveRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlerteReceive.objects.all()
    serializer_class = AlertReceiveSerializers
    lookup_field = "id"

# ================================
#   BLOOD REQUEST
# ================================
class BloodRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    
class BloodRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    lookup_field = "id"


# ================================
#   AUTHENTIFICATION BLOODBANK (JWT)
# ================================
class RegisterBloodBankAPIView(APIView):
    """
    Enregistrer une nouvelle BloodBank.
    """
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        location = request.data.get("location", "")

        if not name or not password or not email:
            return Response({"error": "Tous les champs sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        if BloodBank.objects.filter(name=name).exists():
            return Response({"error": "Ce nom est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)
        if BloodBank.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        bank = BloodBank(
            name=name,
            email=email,
            password=make_password(password),
            location=location
        )
        bank.save()
        serializer = BloodBankSerializer(bank)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginBloodBankAPIView(APIView):
    """
    Connexion pour BloodBank.
    """
    def post(self, request):
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            bank = BloodBank.objects.get(name=name)
        except BloodBank.DoesNotExist:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, bank.password):
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        # Génère JWT
        refresh = RefreshToken.for_user(bank)  # attention : pour JWT natif, BloodBank doit hériter de AbstractBaseUser
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })



class RegisterUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password:
            return Response({"error": "Le nom d'utilisateur et le mot de passe sont obligatoires."},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Ce nom d'utilisateur existe déjà."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Connexion réussie.", "username": user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."},
                            status=status.HTTP_401_UNAUTHORIZED)