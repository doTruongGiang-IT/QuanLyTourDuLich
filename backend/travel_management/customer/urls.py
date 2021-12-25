from django.urls import path

from .views import customer_list, customer_detail, group_customer_detail, group_customer_list

urlpatterns = [
    path('',                        customer_list,                  name='customer-list'),
    path('<int:pk>',                customer_detail,                name='customer-detail'),
    
    path('group/<int:group_id>',    group_customer_detail,          name='group-customer-detail'),
    path('group/',                  group_customer_list,            name='group-customer-list'),
]