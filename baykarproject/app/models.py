from django.db import models
from django.contrib.auth.models import User

class UAV(models.Model):
    UAV_CATEGORIES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.FloatField()
    category = models.CharField(max_length=20, choices=UAV_CATEGORIES)

    def __str__(self):
        return f"{self.brand} {self.model}"


class UAVRental(models.Model):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_start_date = models.DateTimeField()
    rent_end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.uav.brand} {self.uav.model} - Rented by {self.renter.username} from {self.rent_start_date} to {self.rent_end_date}"