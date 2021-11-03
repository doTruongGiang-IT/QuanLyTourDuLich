from django.urls import path

from .views import group_list, group_detail, group_journey_detail, group_journey_list

urlpatterns = [
    path('',                   group_list,                  name='group-list'),
    path('<int:pk>',           group_detail,                name='group-detail'),
    
    path('journey',             group_journey_list,         name='group-journey-list'),
    path('journey/<int:pk>',    group_journey_detail,       name='group-journey-detail'),
]