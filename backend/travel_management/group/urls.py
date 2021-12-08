from django.urls import path

from .views import group_list, group_detail, group_journey_detail, group_journey_list, group_journey_cost_type_list, group_journey_cost_type_detail, group_journey_cost_list, group_journey_cost_detail

urlpatterns = [
    path('',                            group_list,                         name='group-list'),
    path('<int:pk>',                    group_detail,                       name='group-detail'),
    
    path('journey',                     group_journey_list,                 name='group-journey-list'),
    path('journey/<int:pk>',            group_journey_detail,               name='group-journey-detail'),
    
    path('cost',                        group_journey_cost_list,            name='group-journey-cost-list'),
    path('cost/<int:pk>',               group_journey_cost_detail,          name='group-journey-cost-detail'),
    
    path('cost_type',                   group_journey_cost_type_list,       name='group-journey-cost-type-list' ),
    path('cost_type/<int:pk>',          group_journey_cost_type_detail,     name='group-journey-cost-type-detail' ),
]