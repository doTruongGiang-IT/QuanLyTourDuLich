from django.urls import path

from .views import group_list, group_detail

urlpatterns = [
    path('',                   group_list,          name='tour-list'),
    path('<int:pk>',           group_detail,        name='tour-detail'),
]