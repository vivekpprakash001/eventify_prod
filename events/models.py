from django.db import models
from master_data.models import EventType

class Event(models.Model):
    created_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    place = models.CharField(max_length=200)

    is_bookable = models.BooleanField(default=False)

    is_eventify_event = models.BooleanField(default=True)
    outside_event_url = models.URLField(default='NA')

    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_status = models.CharField(max_length=250, choices=[
        ('created', 'Created'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('postponed', 'Postponed'),
    ], default='pending')
    cancelled_reason = models.TextField(default='NA')

    def __str__(self):
        return f"{self.name} ({self.start_date})"

class EventImages(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    event_image = models.ImageField(upload_to='event_images')

    def __str__(self):
        return f"{self.event_image}"
