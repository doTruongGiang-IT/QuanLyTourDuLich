from django.urls import path

from .views import tour_list, tour_detail

urlpatterns = [
    path('',                   tour_list,          name='tour-list'),
    path('<int:pk>',           tour_detail,        name='tour-detail'),
]