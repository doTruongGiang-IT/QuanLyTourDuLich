from rest_framework import serializers

from tour.models import Location
from .models import Group, GroupJourney, GroupJourneyCostType, GroupJourneyCost


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
        
        if self.context.get('is_full_format') is True:
            representation['location'].update({
                'id': location.id,
                'level': location.level
            })
        else:
            del representation['group']
        
        return representation
    
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        is_full_format = True
        if self.context.get('request').query_params.get("tour_id", None):
            del representation['tour']
            is_full_format = False
        
        journeys = GroupJourney.objects.filter(group=instance.id)
        group_journey_serializer = GroupJourneySerializer(journeys, many=True, context={'is_full_format': is_full_format})
        representation['journey'] = group_journey_serializer.data
        
        
        return representation

    
class GroupJourneyCostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupJourneyCostType
        fields = '__all__'
        
        
class GroupJourneyCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupJourneyCost
        fields = '__all__'