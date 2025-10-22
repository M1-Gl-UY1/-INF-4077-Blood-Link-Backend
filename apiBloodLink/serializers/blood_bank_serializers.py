from rest_framework import serializers
from apiBloodLink.models import BloodBank, BloodTransaction


class BloodTransactionSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    blood_bag_name = serializers.CharField(source='blood_bag.name', read_only=True)  # ou un champ qui identifie la poche

    class Meta:
        model = BloodTransaction
        fields = ['id', 'provider', 'provider_name', 'bank', 'bank_name', 'blood_bag', 'blood_bag_name', 'transaction_type', 'date']
        read_only_fields = ["id", "date"]
        


class BloodBankSerializer(serializers.ModelSerializer):
    # Inclure toutes les transactions liées à cette banque
    transactions = BloodTransactionSerializer(source='bloodtransaction_set', many=True, read_only=True)

    class Meta:
        model = BloodBank
        fields = ['id', 'name', 'email', 'transactions']
        read_only_fields = ["id"]
