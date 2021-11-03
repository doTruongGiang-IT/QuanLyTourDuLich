from base.views import PaginateMixin, TrackingMixin
from django.db.models import Q
from rest_framework import viewsets

from .models import Group, GroupJourney
from .serializers import GroupJourneySerializer, GroupSerializer


class GroupViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    object_name = 'group'
    
    def filter_queryset(self, queryset): 
        tour_id = self.request.query_params.get("tour_id", None)
        query = Q()

        if tour_id:
            query = query & Q(tour_id=tour_id)

        queryset = queryset.filter(query)
        return super().filter_queryset(queryset)
    
    
class GroupJourneyViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = GroupJourneySerializer
    queryset = GroupJourney.objects.all()
    object_name = 'group_journey'
    
    def filter_queryset(self, queryset): 
        group_id = self.request.query_params.get("group_id", None)
        query = Q()

        if group_id:
            query = query & Q(group_id=group_id)

        queryset = queryset.filter(query)
        return super().filter_queryset(queryset)
    
group_list = GroupViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

group_detail = GroupViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_journey_list = GroupJourneyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

group_journey_detail = GroupJourneyViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})
