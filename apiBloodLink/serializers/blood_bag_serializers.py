from rest_framework import serializers
from apiBloodLink.models.blood_bag_models import BloodBag



class BloodBagSerializer(serializers.ModelSerializer):
    providerFor_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = BloodBag
        fields = '__all__'
        read_only_fields = ["id"]
        