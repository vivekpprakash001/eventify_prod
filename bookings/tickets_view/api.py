from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from rest_framework.views import APIView

from bookings.models import Ticket
from events.models import Event
from mobile_api.utils import validate_token_and_get_user


def _ticket_to_dict(ticket):
    """
    Helper to serialise a Ticket instance into a simple dict suitable for JSON.
    """
    data = model_to_dict(
        ticket,
        fields=[
            "id",
            "ticket_name",
            "price_per_ticket",
            "maximum_quantity",
            "available_quantity",
            "is_active",
            "created_date",
            "updated_date",
        ],
    )
    data["event_id"] = ticket.event_id
    return data


@method_decorator(csrf_exempt, name="dispatch")
class TicketCreateAPI(APIView):
    """
    Create a new Ticket.

    Expected JSON body (along with token & username used across mobile_api):
    {
        "token": "...",
        "username": "...",
        "event_id": 1,
        "ticket_name": "VIP",
        "price_per_ticket": 1000.0,
        "maximum_quantity": 50,
        "available_quantity": 50,   # optional, defaults to maximum_quantity
        "is_active": true           # optional, defaults to true
    }
    """

    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            event_id = data.get("event_id")
            ticket_name = data.get("ticket_name")
            price_per_ticket = data.get("price_per_ticket")
            maximum_quantity = data.get("maximum_quantity")
            available_quantity = data.get("available_quantity")
            is_active = data.get("is_active", True)

            if not event_id or not ticket_name or price_per_ticket is None or maximum_quantity is None:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "event_id, ticket_name, price_per_ticket and maximum_quantity are required.",
                    },
                    status=400,
                )

            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Event not found."},
                    status=404,
                )

            try:
                price_per_ticket = float(price_per_ticket)
                maximum_quantity = int(maximum_quantity)
                if available_quantity is not None:
                    available_quantity = int(available_quantity)
                else:
                    available_quantity = maximum_quantity
            except (TypeError, ValueError):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "price_per_ticket, maximum_quantity and available_quantity must be numeric.",
                    },
                    status=400,
                )

            if maximum_quantity <= 0:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "maximum_quantity must be greater than zero.",
                    },
                    status=400,
                )

            ticket = Ticket.objects.create(
                event=event,
                ticket_name=ticket_name,
                price_per_ticket=price_per_ticket,
                maximum_quantity=maximum_quantity,
                available_quantity=available_quantity,
                is_active=bool(is_active),
            )

            return JsonResponse(
                {"status": "success", "ticket": _ticket_to_dict(ticket)},
                status=201,
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500,
            )


@method_decorator(csrf_exempt, name="dispatch")
class TicketListAPI(APIView):
    """
    List tickets, optionally filtered by event_id.

    Expected JSON body:
    {
        "token": "...",
        "username": "...",
        "event_id": 1   # optional
    }
    """

    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            event_id = data.get("event_id")

            tickets_qs = Ticket.objects.all().order_by("-created_date")
            if event_id:
                tickets_qs = tickets_qs.filter(event_id=event_id)

            tickets = [_ticket_to_dict(t) for t in tickets_qs]

            return JsonResponse(
                {"status": "success", "tickets": tickets},
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500,
            )


@method_decorator(csrf_exempt, name="dispatch")
class TicketUpdateAPI(APIView):
    """
    Update an existing Ticket.

    Expected JSON body:
    {
        "token": "...",
        "username": "...",
        "ticket_id": 1,
        "ticket_name": "...",           # optional
        "price_per_ticket": 1000.0,     # optional
        "maximum_quantity": 50,         # optional
        "available_quantity": 50,       # optional
        "is_active": true               # optional
    }
    """

    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            ticket_id = data.get("ticket_id")
            if not ticket_id:
                return JsonResponse(
                    {"status": "error", "message": "ticket_id is required."},
                    status=400,
                )

            try:
                ticket = Ticket.objects.get(id=ticket_id)
            except Ticket.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Ticket not found."},
                    status=404,
                )

            # Optional updates
            ticket_name = data.get("ticket_name")
            price_per_ticket = data.get("price_per_ticket")
            maximum_quantity = data.get("maximum_quantity")
            available_quantity = data.get("available_quantity")
            is_active = data.get("is_active")

            if ticket_name is not None:
                ticket.ticket_name = ticket_name

            try:
                if price_per_ticket is not None:
                    ticket.price_per_ticket = float(price_per_ticket)
                if maximum_quantity is not None:
                    maximum_quantity = int(maximum_quantity)
                    if maximum_quantity <= 0:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "maximum_quantity must be greater than zero.",
                            },
                            status=400,
                        )
                    ticket.maximum_quantity = maximum_quantity
                if available_quantity is not None:
                    ticket.available_quantity = int(available_quantity)
            except (TypeError, ValueError):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "price_per_ticket, maximum_quantity and available_quantity must be numeric.",
                    },
                    status=400,
                )

            if is_active is not None:
                ticket.is_active = bool(is_active)

            ticket.save()

            return JsonResponse(
                {"status": "success", "ticket": _ticket_to_dict(ticket)},
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500,
            )


@method_decorator(csrf_exempt, name="dispatch")
class TicketDeleteAPI(APIView):
    """
    Delete an existing Ticket.

    Expected JSON body:
    {
        "token": "...",
        "username": "...",
        "ticket_id": 1
    }
    """

    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            ticket_id = data.get("ticket_id")
            if not ticket_id:
                return JsonResponse(
                    {"status": "error", "message": "ticket_id is required."},
                    status=400,
                )

            try:
                ticket = Ticket.objects.get(id=ticket_id)
            except Ticket.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Ticket not found."},
                    status=404,
                )

            ticket.delete()

            return JsonResponse(
                {"status": "success", "message": "Ticket deleted successfully."},
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500,
            )

