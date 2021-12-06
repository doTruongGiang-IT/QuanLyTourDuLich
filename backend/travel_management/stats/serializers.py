from rest_framework import serializers

from customer.models import GroupCustomer
from staff.models import Staff, GroupStaff
from group.models import Group, GroupJourneyCost


class StatsToursOfStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        number_of_tours = len(GroupStaff.objects.filter(staff=instance.id))
        representation['number_of_tours'] = number_of_tours  
        
        return representation
    
    
class StatsCostRevenueGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        del representation['start_date']
        del representation['end_date']
        del representation['tour']
        
        group_costs = GroupJourneyCost.objects.filter(group=instance.id)
        total_of_cost = 0
        
        for cost in group_costs:
            total_of_cost += cost.price
            
        number_of_guests = GroupCustomer.objects.filter(group=instance.id).__len__()
        revenue = number_of_guests * instance.tour.price.price
        representation['cost'] = total_of_cost
        representation['revenue'] = revenue
          
        return representation
    