from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from events.models import Event, EventImages
from master_data.models import EventType
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime, timedelta
import calendar
from mobile_api.utils import validate_token_and_get_user


@method_decorator(csrf_exempt, name='dispatch')
class EventTypeListAPIView(APIView):

    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            # Fetch event types manually without serializer
            event_types_queryset = EventType.objects.all()
            event_types = []
            
            for event_type in event_types_queryset:
                event_type_data = {
                    "id": event_type.id,
                    "event_type": event_type.event_type,
                    "event_type_icon": request.build_absolute_uri(event_type.event_type_icon.url) if event_type.event_type_icon else None
                }
                event_types.append(event_type_data)

            print(event_types)

            return JsonResponse({
                "status": "success",
                "event_types": event_types
            })

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventListAPI(APIView):

    def post(self, request):
        try:
            print('*' * 100)
            print(request.body)
            print('*' * 100)
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            pincode = data.get("pincode")
            print('*' * 100)
            print(pincode)
            print('*' * 100)
            # pincode is optional - if not provided or 'all', return all events
            if not pincode or pincode == 'all':
                events = Event.objects.all().order_by('-created_date')
            else:
                events = Event.objects.filter(pincode=pincode).order_by('-created_date')
            
            event_list = []

            for e in events:
                data_dict = model_to_dict(e)
                try:
                    thumb_img = EventImages.objects.get(event=e.id, is_primary=True)
                    data_dict['thumb_img'] = request.build_absolute_uri(thumb_img.event_image.url)
                except EventImages.DoesNotExist:
                    data_dict['thumb_img'] = ''

                event_list.append(data_dict)

            print('*' * 100)
            print(event_list)
            print('*' * 100)

            return JsonResponse({
                "status": "success",
                "events": event_list
            })

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventDetailAPI(APIView):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            event_id = data.get("event_id")

            events = Event.objects.get(id=event_id)
            event_images = EventImages.objects.filter(event=event_id)
            event_data = model_to_dict(events)
            event_data["status"] = "success"
            event_images_list = []
            for ei in event_images:
                event_img = {}
                event_img['is_primary'] = ei.is_primary
                event_img['image'] = request.build_absolute_uri(ei.event_image.url)
                event_images_list.append(event_img)
            event_data["images"] = event_images_list

            print(event_data)

            return JsonResponse(event_data)

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventImagesListAPI(APIView):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            event_id = data.get("event_id")

            event_images = EventImages.objects.filter(event=event_id)
            res_data = {}
            res_data["status"] = "success"
            event_images_list = []
            for ei in event_images:
                event_images_list.append(request.build_absolute_uri(ei.event_image.url))

            res_data["images"] = event_images_list

            print(res_data)

            return JsonResponse(res_data)

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


@method_decorator(csrf_exempt, name='dispatch')
class EventsByCategoryAPI(APIView):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response

            category_id = data.get("category_id")

            if not category_id:
                return JsonResponse(
                    {"status": "error", "message": "category_id is required"}
                )

            events = Event.objects.filter(event_type=category_id)
            events_dict = [model_to_dict(obj) for obj in events]

            for event in events_dict:
                try:
                    event['event_image'] = request.build_absolute_uri(
                        EventImages.objects.get(event=event['id'], is_primary=True).event_image.url
                    )
                except EventImages.DoesNotExist:
                    event['event_image'] = ''
                # event['start_date'] = convert_date_to_dd_mm_yyyy(event['start_date'])
            print(events_dict)

            return JsonResponse({
                "status": "success",
                "events": events_dict
            })

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


@method_decorator(csrf_exempt, name='dispatch')
class EventsByMonthYearAPI(APIView):
    """
    API to get events by month and year.
    Returns dates that have events, total count, and date-wise breakdown.
    """
    
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response
            
            month_name = data.get("month")  # e.g., "August", "august", "Aug"
            year = data.get("year")  # e.g., 2025
            
            if not month_name or not year:
                return JsonResponse(
                    {"status": "error", "message": "month and year are required"}
                )
            
            # Convert month name to month number
            month_name_lower = month_name.lower().capitalize()
            month_abbr = month_name_lower[:3]
            
            # Try full month name first, then abbreviation
            month_number = None
            for i in range(1, 13):
                if calendar.month_name[i].lower() == month_name_lower or calendar.month_abbr[i].lower() == month_abbr.lower():
                    month_number = i
                    break
            
            if not month_number:
                return JsonResponse(
                    {"status": "error", "message": f"Invalid month name: {month_name}"}
                )
            
            # Convert year to integer
            try:
                year = int(year)
            except (ValueError, TypeError):
                return JsonResponse(
                    {"status": "error", "message": "Invalid year format"}
                )
            
            # Filter events where start_date or end_date falls in the given month/year
            # An event is included if any part of it (start_date to end_date) overlaps with the month
            # events = Event.objects.filter(
            #     Q(start_date__year=year, start_date__month=month_number) |
            #     Q(end_date__year=year, end_date__month=month_number) |
            #     Q(start_date__lte=datetime(year, month_number, 1).date(),
            #       end_date__gte=datetime(year, month_number, calendar.monthrange(year, month_number)[1]).date())
            # ).distinct()

            events = Event.objects.filter(start_date__year=year, start_date__month=month_number).distinct()
            print('*' * 100)
            print(f'Total events: {events.count()}')
            print('*' * 100)
            unique_start_dates = events.values_list('start_date', flat=True).distinct()
            date_strings = [d.strftime('%Y-%m-%d') for d in unique_start_dates]
            print('*' * 100)
            print(f'Unique start dates: {date_strings}')
            print('*' * 100)

            
            # Group events by date
            date_events_dict = {}
            all_dates = set()
            
            # Calculate month boundaries
            month_start = datetime(year, month_number, 1).date()
            month_end = datetime(year, month_number, calendar.monthrange(year, month_number)[1]).date()
            
            for event in events:
                # Get all dates between start_date and end_date that fall in the target month
                current_date = max(event.start_date, month_start)
                end_date = min(event.end_date, month_end)
                
                # Iterate through each date in the event's date range that falls in the target month
                while current_date <= end_date:
                    if current_date.year == year and current_date.month == month_number:
                        date_str = current_date.strftime('%Y-%m-%d')
                        all_dates.add(date_str)
                        if date_str not in date_events_dict:
                            date_events_dict[date_str] = 0
                        date_events_dict[date_str] += 1
                    
                    # Move to next day
                    current_date += timedelta(days=1)
            
            # Sort dates
            sorted_dates = sorted(all_dates)
            
            # Build date_events list
            date_events = [
                {
                    "date_of_event": date_str,
                    "events_of_date": date_events_dict[date_str]
                }
                for date_str in sorted_dates
            ]
            
            # Calculate total number of events (unique events, not date occurrences)
            total_events = events.count()

            print(sorted_dates)
            print(total_events)
            print(date_events)
            
            return JsonResponse({
                "status": "success",
                "dates": date_strings,
                "total_number_of_events": total_events,
                "date_events": date_events
            })
                
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


@method_decorator(csrf_exempt, name='dispatch')
class EventsByDateAPI(APIView):
    """
    API to get events occurring on a specific date.
    Returns complete event information with primary images.
    """
    
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request)
            if error_response:
                return error_response
            
            date_of_event = data.get("date_of_event")
            
            if not date_of_event:
                return JsonResponse(
                    {"status": "error", "message": "date_of_event is required"}
                )
            
            # Parse date_of_event in YYYY-MM-DD format
            try:
                event_date = datetime.strptime(date_of_event, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid date format. Expected YYYY-MM-DD"}
                )
            
            # Filter events where the provided date falls between start_date and end_date (inclusive)
            events = Event.objects.filter(
                start_date=event_date
            ).order_by('start_date')
            
            event_list = []
            
            for e in events:
                data_dict = model_to_dict(e)
                try:
                    thumb_img = EventImages.objects.get(event=e.id, is_primary=True)
                    data_dict['thumb_img'] = request.build_absolute_uri(thumb_img.event_image.url)
                except EventImages.DoesNotExist:
                    data_dict['thumb_img'] = ''
                
                event_list.append(data_dict)
            
            return JsonResponse({
                "status": "success",
                "events": event_list
            })
                
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )