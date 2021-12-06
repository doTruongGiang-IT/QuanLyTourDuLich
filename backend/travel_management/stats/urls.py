from django.urls import path

from .views import stats_tour_staff_list, stats_cost_revenue_group_list

urlpatterns = [
    path('tour_of_staff',                       stats_tour_staff_list,                  name='stats-tour-staff-list'),
    path('stats_cost_revenue_group_list/<int:pk>',       stats_cost_revenue_group_list,          name='stats-cost-revenue-group-list'),
]