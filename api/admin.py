from django.contrib import admin
from .models import User, ParkingLot, ParkingSpace, Reservation, Vehicle

admin.site.register(User)
admin.site.register(ParkingLot)
admin.site.register(ParkingSpace)
admin.site.register(Reservation)
admin.site.register(Vehicle)
