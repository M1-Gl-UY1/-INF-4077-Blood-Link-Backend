from rest_framework import serializers
from apiBloodLink.models.blood_bag_models import BloodBag



class BloodBagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBag
        fields = '__all__'
        read_only_fields = ["id"]
        