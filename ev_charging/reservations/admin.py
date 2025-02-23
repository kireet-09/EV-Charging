from django.contrib import admin
from .models import Station, Slot, Reservation

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_slots')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'station', 'is_available')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'slot', 'start_time', 'end_time')
