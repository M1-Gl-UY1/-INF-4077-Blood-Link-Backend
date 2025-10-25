from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apiBloodLink import serializers

from ..service.reply_service import reply_to_alert

from ..models.alertReceive_models import AlerteReceive
from ..serializers.alertReceive_serializers import AlertReceiveSerializers

class ReplyCreateAPIView(APIView):
    def post(self, request, alert_id):
        provider_id = request.data.get("provider_id")
        
        if not provider_id:
            return Response({"errors":"provider_id manquant"}, status = status.HTTP_400_BAD_REQUEST)
        
        reply = reply_to_alert(alert_id, provider_id)
        
        if reply:
            serializer = AlertReceiveSerializers(reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Réponse déjà existante ou alerte introuvable"}, status=status.HTTP_400_BAD_REQUEST)