from django.contrib import admin

from .models import Staff, StaffType, GroupStaff

admin.site.register(Staff)
admin.site.register(StaffType)
admin.site.register(GroupStaff)