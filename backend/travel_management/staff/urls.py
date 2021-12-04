from django.urls import path

from .views import staff_list, staff_detail, staff_type_list, staff_type_detail, group_staff_detail, group_staff_list

urlpatterns = [
    path('',                        staff_list,                     name='staff-list'),
    path('<int:pk>',                staff_detail,                   name='staff-detail'),
    
    path('staff_type/',             staff_type_list,                name='staff-type-list'),
    path('staff_type/<int:pk>',     staff_type_detail,              name='staff-type-detail'),
    
    path('group/<int:group_id>',    group_staff_detail,             name='group-staff-detail'),
    path('group/',                  group_staff_list,               name='group-staff-list'),
]