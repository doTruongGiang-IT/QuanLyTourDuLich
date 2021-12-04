from django.urls import path

from .views import stats_tour_staff_detail

urlpatterns = [
    path('tour_of_staff',       stats_tour_staff_detail,        name='stats-tour-staff-detail'),
]