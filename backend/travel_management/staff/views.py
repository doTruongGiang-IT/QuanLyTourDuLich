from base.views import PaginateMixin, TrackingMixin
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from group.models import Group
from .models import Staff, StaffType, GroupStaff
from .serializers import StaffSerializer, StaffTypeSerializer, GroupStaffSerializer


class StaffViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    object_name = 'staff'
   
   
class StaffTypeViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = StaffTypeSerializer
    queryset = StaffType.objects.all()
    object_name = 'staff_type' 


class GroupStaffViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = GroupStaffSerializer
    queryset = GroupStaff.objects.all()
    object_name = 'group_staff'

    def filter_queryset(self, queryset): 
        group_id = self.kwargs.get('group_id', None)
        query = Q()

        if group_id:
            query = query & Q(group_id=group_id)

        queryset = queryset.filter(query)
        return super().filter_queryset(queryset)
        
    def get_object(self):
        group_id = self.request.query_params.get("group_id", None)
        staff_id = self.request.query_params.get("staff_id", None)
        
        if group_id is None or staff_id is None:
            raise ValidationError({"detail": "missing param"})
        
        group_staff = GroupStaff.objects.filter(group_id=group_id, staff_id=staff_id)
        
        if len(group_staff) == 0:
            raise ValidationError({"detail": "staff is not in specific group"})
            
        group_staff = group_staff[0]
        return group_staff
    
    def create(self, request, *args, **kwargs):
        group = request.data['group']
        staff = request.data['staff']
        
        if group and staff:
            group = Group.objects.filter(id=group)
            if group:
                group = group[0]
                groups = GroupStaff.objects.filter(staff_id=staff)
                for g in groups:
                    if g.group.tour_id == group.tour_id:
                        raise ValidationError({"detail": "staff is in the same tour"})
                        
        return super().create(request, *args, **kwargs)
    
    
staff_list = StaffViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

staff_detail = StaffViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

staff_type_list = StaffTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

staff_type_detail = StaffTypeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_staff_list = GroupStaffViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'
})

group_staff_detail = GroupStaffViewSet.as_view({
    'get': 'list'
})