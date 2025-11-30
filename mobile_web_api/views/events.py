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
                    event_list.append(model_to_dict(e))

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
                data = model_to_dict(events)
                data["status"] = "success"

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        images = EventImages.objects.filter(event_id=event_id)

        image_list = [model_to_dict(i) for i in images]

        return JsonResponse({"status": True, "images": image_list}, safe=False)
