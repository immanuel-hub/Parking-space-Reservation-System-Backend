from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [('driver', 'Driver'), ('admin', 'Admin')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='driver')
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.location} "

class ParkingSpace(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('occupied', 'Occupied')]
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='spaces')
    space_number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('parking_lot', 'space_number')
        ordering = ['space_number']

    def __str__(self):
        return f"Space {self.space_number} in {self.parking_lot.name}"

    def is_taken(self):
        return self.status in ['reserved', 'occupied']

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [('car', 'Car'), ('motorcycle', 'Motorcycle'), ('truck', 'Truck')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='car')

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"   