from django.contrib import admin

from .models import Customer, GroupCustomer

admin.site.register(Customer)
admin.site.register(GroupCustomer)