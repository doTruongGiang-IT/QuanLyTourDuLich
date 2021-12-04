from base.views import PaginateMixin, TrackingMixin
from rest_framework import viewsets

from staff.models import Staff
from .serializers import StatsToursOfStaffSerializer


class StatsToursOfStaffViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = StatsToursOfStaffSerializer
    queryset = Staff.objects.all()
    object_name = 'stats_tour_staff'
    
    
stats_tour_staff_detail = StatsToursOfStaffViewSet.as_view({
    'get': 'list'
})