from django.contrib import admin
from .models import Tour, TourCharacteristic, TourPrice, TourType, Location


admin.site.register(Tour)
admin.site.register(TourCharacteristic)
admin.site.register(TourPrice)
admin.site.register(TourType)
admin.site.register(Location)