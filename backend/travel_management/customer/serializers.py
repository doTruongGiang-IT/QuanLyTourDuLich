from rest_framework import serializers

from .models import Customer, GroupCustomer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

        
class GroupCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCustomer
        fields = '__all__'
    