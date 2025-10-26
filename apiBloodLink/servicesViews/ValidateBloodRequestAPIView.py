from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apiBloodLink.service.blood_request_service import validate_request_and_create_alert 
from apiBloodLink.serializers.alert_Serializers import AlertSerializer


class ValidateBloodRequestAPIView(APIView):
    def post(self, request, request_id):
        alert = validate_request_and_create_alert(request_id)

        if alert:
            serializer = AlertSerializer(alert)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": f"Requête {alert} introuvable ou déjà traitée."},
        status=status.HTTP_400_BAD_REQUEST
        )
