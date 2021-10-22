from rest_framework import viewsets

from .models import Tour
from .serializers import TourSerializer


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    queryset = Tour.objects.all()
    
    
tour_list = TourViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tour_detail = TourViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})
