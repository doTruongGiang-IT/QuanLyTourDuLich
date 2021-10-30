from rest_framework import viewsets

from .models import Tour, TourCharacteristic, TourType, TourPrice, Location
from .serializers import TourSerializer, TourCharacteristicSerializer, TourTypeSerializer, TourPriceSerializer, LocationSerializer


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    queryset = Tour.objects.all()
    
    
class TourCharacteristicViewSet(viewsets.ModelViewSet):
    serializer_class = TourCharacteristicSerializer
    queryset = TourCharacteristic.objects.all()
    
    
class TourTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TourTypeSerializer
    queryset = TourType.objects.all()
    
    
class TourPriceViewSet(viewsets.ModelViewSet):
    serializer_class = TourPriceSerializer
    queryset = TourPrice.objects.all()
    
    
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    
    
tour_list = TourViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tour_detail = TourViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tour_characteristic_list = TourCharacteristicViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tour_characteristic_detail = TourCharacteristicViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tour_type_list = TourTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tour_type_detail = TourTypeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tour_price_list = TourPriceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

tour_price_detail = TourPriceViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

location_list = LocationViewSet.as_view({
    'get': 'list'
})