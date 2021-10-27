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
    
    
class TourCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCharacteristic
        fields = '__all__'
    
    
class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = '__all__'
    
    
class TourPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPrice
        fields = '__all__'
        

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'