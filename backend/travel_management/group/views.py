from django.db.models import Q
from rest_framework import viewsets

from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    
    def filter_queryset(self, queryset): 
        tour_id = self.request.query_params.get("tour_id", None)
        query = Q()

        if tour_id:
            query = query & Q(tour_id=tour_id)

        queryset = queryset.filter(query)
        return super().filter_queryset(queryset)
    
    
group_list = GroupViewSet.as_view({
    'get': 'list'
})

group_detail = GroupViewSet.as_view({
    'get': 'retrieve'
})
