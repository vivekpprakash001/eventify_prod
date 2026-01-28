from django.urls import path

from bookings.tickets_view.api import (
    TicketCreateAPI,
    TicketListAPI,
    TicketUpdateAPI,
    TicketDeleteAPI,
)


urlpatterns = [
    path("tickets/create/", TicketCreateAPI.as_view(), name="ticket_create"),
    path("tickets/list/", TicketListAPI.as_view(), name="ticket_list"),
    path("tickets/update/", TicketUpdateAPI.as_view(), name="ticket_update"),
    path("tickets/delete/", TicketDeleteAPI.as_view(), name="ticket_delete"),
]

