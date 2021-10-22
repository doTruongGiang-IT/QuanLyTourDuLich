from rest_framework import serializers

from .models import Tour, TourCharacteristic, TourType, TourPrice, Location


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        characteristic  = representation['characteristic'] 
        tour_type       = representation['type'] 
        price           = representation['price'] 
        location        = representation['location'] 
        
        characteristic  = TourCharacteristic.objects.get(pk=characteristic)
        tour_type       = TourType.objects.get(pk=tour_type)
        price           = TourPrice.objects.get(pk=price)
        location        = Location.objects.get(pk=location)
        
        representation['characteristic']    = characteristic.name
        representation['type']              = tour_type.name
        representation['price_name']        = price.name
        representation['price']             = price.price
        representation['location']          = location.name
        
        return representation