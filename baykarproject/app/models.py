from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
    user_info = models.CharField(max_length=200, blank=True, null=True)
    user_email = models.CharField(max_length=200, blank=True, null=True)
    uav_info = models.CharField(max_length=200, blank=True, null=True) 
    rent_start_date = models.DateTimeField()
    rent_end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.uav.brand} {self.uav.model} - Rented by {self.renter.username} from {self.rent_start_date} to {self.rent_end_date}"

    def save(self, *args, **kwargs):
        self.user_info = f"{self.renter.first_name} {self.renter.last_name}"
        self.uav_info = f"{self.uav.brand} {self.uav.model}"
        self.user_email = f"{self.renter.email}"
        super().save(*args, **kwargs)

    def clean(self):
        # check if the UAV is already rented during the specified period
        # remaining part is unimplemented
        if UAVRental.objects.filter(
            uav=self.uav,
            rent_end_date__gt=self.rent_start_date,
            rent_start_date__lt=self.rent_end_date
        ).exclude(pk=self.pk).exists():
            raise ValidationError("This UAV is already rented during the specified period.")
