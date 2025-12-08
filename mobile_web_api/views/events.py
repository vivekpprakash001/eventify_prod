from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from events.models import Event, EventImages
from rest_framework.authtoken.models import Token
from master_data.models import EventType
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required


@method_decorator(csrf_exempt, name='dispatch')
class EventTypeListAPIView(APIView):

    def post(self, request):
        try:
            # Manually load JSON because we are not using parsers
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"}
                )

            try:
                token = Token.objects.get(key=token_key)
                user = token.user

                if user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"}
                    )

                # Fetch event types manually without serializer
                event_types = list(EventType.objects.values("id", "event_type"))

                return JsonResponse({
                    "status": "success",
                    "event_types": event_types
                })

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventListAPI(APIView):

    def post(self, request):
        try:
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")
            pincode = data.get("pincode")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"}
                )

            try:
                token = Token.objects.get(key=token_key)
                user = token.user

                if user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"}
                    )

                events = Event.objects.filter(pincode=pincode).order_by('-created_date')
                event_list = []

                for e in events:
                    data_dict = model_to_dict(e)
                    print('*' * 10)
                    print(e.id)
                    print('*' * 10)
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

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventDetailAPI(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")
            event_id = data.get("event_id")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"}
                )

            try:
                token = Token.objects.get(key=token_key)
                user = token.user

                if user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"}
                    )

                events = Event.objects.get(id=event_id)
                event_images = EventImages.objects.filter(event=event_id)
                data = model_to_dict(events)
                data["status"] = "success"
                event_images_list = []
                for ei in event_images:
                    event_img = {}
                    event_img['is_primary'] = ei.is_primary
                    event_img['image'] = request.build_absolute_uri(ei.event_image.url)
                    event_images_list.append(event_img)
                data["images"] = event_images_list

                return JsonResponse(data)

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


class EventImagesListAPI(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")
            event_id = data.get("event_id")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"}
                )

            try:
                token = Token.objects.get(key=token_key)
                user = token.user

                if user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"}
                    )

                event_images = EventImages.objects.filter(event=event_id)
                res_data = {}
                res_data["status"] = "success"
                event_images_list = []
                for ei in event_images:
                    event_images_list.append(request.build_absolute_uri(ei.event_image.url))

                res_data["images"] = event_images_list

                return JsonResponse(res_data)

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
            )


@login_required(login_url="login")
def api_events_by_category(request, slug):
    events = Event.objects.filter(event_type=slug)

    events_dict = [model_to_dict(obj) for obj in events]

    for event in events_dict:
        event['event_image'] = EventImages.objects.get(event=event['id'], is_primary=True).event_image.url
        # event['start_date'] = convert_date_to_dd_mm_yyyy(event['start_date'])

    return JsonResponse({"events": events_dict})