from rest_framework import serializers

from .models import Staff, StaffType, GroupStaff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffType
        fields = '__all__'
        
        
class GroupStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStaff
        fields = '__all__'
    