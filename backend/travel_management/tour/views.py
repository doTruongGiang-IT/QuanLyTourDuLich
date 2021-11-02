from rest_framework import viewsets

from base.views import TrackingMixin
from .models import Tour, TourCharacteristic, TourType, TourPrice, Location
from .serializers import TourSerializer, TourCharacteristicSerializer, TourTypeSerializer, TourPriceSerializer, LocationSerializer


class TourViewSet(TrackingMixin, viewsets.ModelViewSet):
    serializer_class = TourSerializer
    queryset = Tour.objects.all()
    object_name = 'tour'
    
    def get_serializer_context(self):
        contexts = super().get_serializer_context()
        
        is_format = self.request.query_params.get("is_format", None)
        if is_format is not None and is_format == 'true':
            contexts['is_format'] = True 
        else:
            contexts['is_format'] = False
        
        return contexts
    
    
class TourCharacteristicViewSet(TrackingMixin, viewsets.ModelViewSet):
    serializer_class = TourCharacteristicSerializer
    queryset = TourCharacteristic.objects.all()
    object_name = 'tour_characteristic'
    
    
class TourTypeViewSet(TrackingMixin, viewsets.ModelViewSet):
    serializer_class = TourTypeSerializer
    queryset = TourType.objects.all()
    object_name = 'tour_type'
    
    
class TourPriceViewSet(TrackingMixin, viewsets.ModelViewSet):
    serializer_class = TourPriceSerializer
    queryset = TourPrice.objects.all()
    object_name = 'tour_price'
    
    
class LocationViewSet(TrackingMixin, viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    object_name = 'location'
    
    
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
    'get': 'list',
    'post': 'create'
})

location_detail = LocationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})