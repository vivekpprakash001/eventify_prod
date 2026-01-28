from django.db import models
import uuid
from events.models import Event
from accounts.models import User

# Create your models here.
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_name = models.CharField(max_length=250)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_quantity = models.IntegerField()
    available_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.ticket_name


class TicketType(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=250)
    ticket_type_description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    is_offer = models.BooleanField(default=False)
    offer_percentage = models.IntegerField(default=0)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    offer_start_date = models.DateField(blank=True, null=True)
    offer_end_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.ticket_type


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.user.username + " - " + self.ticket.event.name


class Booking(models.Model):
    booking_id = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    transaction_id = models.CharField(max_length=250, blank=True, null=True)

    def __save__(self):
        if not self.booking_id:
            self.booking_id = str(self.ticket.event.name[:3].upper()) + str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_id