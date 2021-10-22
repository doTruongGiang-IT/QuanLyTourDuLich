from rest_framework import serializers

from .models import Tour, TourCharacteristic, TourType, TourPrice, Location


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['characteristic']    = instance.characteristic.name
        representation['type']              = instance.type.name
        representation['price_name']        = instance.price.name
        representation['price']             = instance.price.price
        representation['location']          = instance.location.name
        
        return representation