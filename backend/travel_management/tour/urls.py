from django.urls import path

from .views import (
    tour_list,
    tour_detail,
    tour_characteristic_list,
    tour_characteristic_detail,
    tour_type_list,
    tour_price_list,
    tour_price_detail,
    location_list
)

urlpatterns = [
    path('',                            tour_list,                  name='tour-list'),
    path('<int:pk>',                    tour_detail,                name='tour-detail'),
    
    path('tour_characteristic',         tour_characteristic_list,   name='tour-characteristic-list'),
    path('tour_characteristic/<int:pk>',tour_characteristic_detail, name='tour-characteristic-detail'),
    
    path('tour_type',                   tour_type_list,             name='tour-type-list'),
    
    path('tour_price',                  tour_price_list,            name='tour-price-list'),
    path('tour_price/<int:pk>',         tour_price_detail,          name='tour-price-detail'),
    
    path('location',                    location_list,              name='location-list'),
]