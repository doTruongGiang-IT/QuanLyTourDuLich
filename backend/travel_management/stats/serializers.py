from rest_framework import serializers
from collections import OrderedDict
from staff.models import Staff, GroupStaff


class StatsToursOfStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        number_of_tours = len(GroupStaff.objects.filter(staff=instance.id))
        representation['number_of_tours'] = number_of_tours  
        
        return representation
    