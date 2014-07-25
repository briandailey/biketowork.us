from django.contrib import admin

# Register your models here.

from .models import Ride

class RideAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'minutes', 'distance')

admin.site.register(Ride, RideAdmin)
