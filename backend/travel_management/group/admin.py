from django.contrib import admin

from .models import Group, GroupJourney, GroupJourneyCostType, GroupJourneyCost

admin.site.register(Group)
admin.site.register(GroupJourney)
admin.site.register(GroupJourneyCost)
admin.site.register(GroupJourneyCostType)