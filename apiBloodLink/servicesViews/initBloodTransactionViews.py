from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apiBloodLink.service.initBloodTransactionService import TransactionCreateView
from apiBloodLink.serializers.blood_bank_serializers import BloodTransactionSerializer


class ValidateinitBloodTransactionViewsView(APIView):
    def post(self, request):
        provider_id = request.data.get("provider_id")
        bank_id = request.data.get("bank_id")
        
        bloodTransaction = TransactionCreateView(provider_id, bank_id)

        if bloodTransaction:
            serializer = BloodTransactionSerializer(bloodTransaction)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": f"Requête {bloodTransaction} introuvable ou déjà traitée."},
        status=status.HTTP_400_BAD_REQUEST
        )
