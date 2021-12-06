from django.db.models import query
from base.views import PaginateMixin, TrackingMixin
from rest_framework import serializers, viewsets

from group.models import Group
from staff.models import Staff
from .serializers import StatsToursOfStaffSerializer, StatsCostRevenueGroupSerializer


class StatsToursOfStaffViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = StatsToursOfStaffSerializer
    queryset = Staff.objects.all()
    object_name = 'stats_tour_staff'
    

class StatsCostRevenueGroupViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = StatsCostRevenueGroupSerializer
    object_name = 'stats_cost_revenue_group'
    
    def get_queryset(self):
        tour_id = self.kwargs['pk']
        queryset = Group.objects.filter(tour=tour_id)
        
        return queryset
   
    
stats_tour_staff_list = StatsToursOfStaffViewSet.as_view({
    'get': 'list'
})

stats_cost_revenue_group_list = StatsCostRevenueGroupViewSet.as_view({
    'get': 'list'
})