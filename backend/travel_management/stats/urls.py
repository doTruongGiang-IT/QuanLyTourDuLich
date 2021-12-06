from django.urls import path

from .views import stats_tour_staff_list, stats_cost_revenue_group_list, stats_cost_revenue_tour_list

urlpatterns = [
    path('tour_of_staff',                               stats_tour_staff_list,                  name='stats-tour-staff-list'),
    path('stats_cost_revenue_group/<int:pk>',           stats_cost_revenue_group_list,          name='stats-cost-revenue-group-list'),
    path('stats_cost_revenue_tour',            stats_cost_revenue_tour_list,           name='stats-cost-revenue-tour-list'),
]