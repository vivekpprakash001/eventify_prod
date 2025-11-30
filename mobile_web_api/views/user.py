# accounts/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from mobile_web_api.forms import RegisterForm, LoginForm
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = RegisterForm(data)
            if form.is_valid():
                user = form.save()
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'User registered successfully', 'token': token.key}, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            if form.is_valid():
                user = form.cleaned_data['user']
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'Login successful', 'token': token.key})
            return JsonResponse({'errors': form.errors}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"},
                    status=400
                )

            try:
                token = Token.objects.get(key=token_key)

                if token.user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"},
                        status=401
                    )

                return JsonResponse({
                    "status": "logged_in",
                    "username": token.user.username,
                    "email": token.user.email
                })

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            token_key = data.get("token")
            username = data.get("username")

            if not token_key or not username:
                return JsonResponse(
                    {"status": "error", "message": "token and username required"},
                    status=400
                )

            try:
                token = Token.objects.get(key=token_key)
                user = token.user

                if user.username != username:
                    return JsonResponse(
                        {"status": "error", "message": "token does not match user"},
                        status=401
                    )

                # 🔍 Call Django's built-in logout
                logout(request)

                # 🗑 Delete the token to invalidate future access
                token.delete()

                return JsonResponse({
                    "status": "logged_out",
                    "message": "Logout successful"
                })

            except Token.DoesNotExist:
                return JsonResponse({"status": "invalid_token"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
