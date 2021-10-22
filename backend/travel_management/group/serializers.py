from rest_framework import serializers

from tour.models import Location
from .models import Group, GroupJourney


class GroupJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupJourney
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        location = representation['location']
        location = Location.objects.get(pk=location)
        
        representation['location'] = {
            'name': location.name,
            'type': location.type
        }
        
        del representation['group']
        
        return representation
    
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('revenue', )
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        journeys = GroupJourney.objects.filter(group=instance.id)
        group_journey_serializer = GroupJourneySerializer(journeys, many=True)
        representation['journey'] = group_journey_serializer.data
        
        del representation['tour']
        
        return representation