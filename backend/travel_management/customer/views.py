from base.views import PaginateMixin, TrackingMixin
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from group.models import Group
from .models import Customer, GroupCustomer
from .serializers import CustomerSerializer, GroupCustomerSerializer


class CustomerViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    object_name = 'customer'
    

class GroupCustomerViewSet(TrackingMixin, PaginateMixin, viewsets.ModelViewSet):
    serializer_class = GroupCustomerSerializer
    queryset = GroupCustomer.objects.all()
    object_name = 'group_customer'

    def filter_queryset(self, queryset): 
        group_id = self.kwargs.get('group_id', None)
        query = Q()

        if group_id:
            query = query & Q(group_id=group_id)

        queryset = queryset.filter(query)
        return super().filter_queryset(queryset)
        
    def get_object(self):
        group_id = self.request.query_params.get("group_id", None)
        customer_id = self.request.query_params.get("customer_id", None)
        
        if group_id is None or customer_id is None:
            raise ValidationError({"detail": "missing param"})
        
        group_customer = GroupCustomer.objects.filter(group_id=group_id, customer_id=customer_id)
        
        if len(group_customer) == 0:
            raise ValidationError({"detail": "customer is not in specific group"})
            
        group_customer = group_customer[0]
        return group_customer
    
    def create(self, request, *args, **kwargs):
        group = request.data['group']
        customer = request.data['customer']
        
        if group and customer:
            group = Group.objects.filter(id=group)
            if group:
                group = group[0]
                groups = GroupCustomer.objects.filter(customer_id=customer)
                for g in groups:
                    if g.group.tour_id == group.tour_id:
                        raise ValidationError({"detail": "customer is in the same tour"})
                        
        return super().create(request, *args, **kwargs)
    
    
customer_list = CustomerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

customer_detail = CustomerViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_customer_list = GroupCustomerViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'
})

group_customer_detail = GroupCustomerViewSet.as_view({
    'get': 'list'
})