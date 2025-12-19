from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.manager import UserManager

ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')

    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    # Location fields
    pincode = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=200, blank=True, null=True)

    # Location fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='default.png')

    objects = UserManager()

    def __str__(self):
        return self.username
