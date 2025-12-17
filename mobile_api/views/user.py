# accounts/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from mobile_api.forms import RegisterForm, LoginForm
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout
from mobile_api.utils import validate_token_and_get_user
from utils.errors_json_convertor import simplify_form_errors


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
        print('0')
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            print('1')
            if form.is_valid(): 
                print('2')
                user = form.cleaned_data['user']
                token, _ = Token.objects.get_or_create(user=user)
                print('3')
                response = {
                    'message': 'Login successful', 
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'pincode': user.pincode,
                    'district': user.district,
                    'state': user.state,
                    'country': user.country,
                    'place': user.place,
                    'latitude': user.latitude,
                    'longitude': user.longitude,
                }
                print('4')
                print(response)
                return JsonResponse(response, status=200)
            
            return JsonResponse(simplify_form_errors(form), status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StatusView(View):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request, error_status_code=True)
            if error_response:
                return error_response

            return JsonResponse({
                "status": "logged_in",
                "username": user.username,
                "email": user.email
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            user, token, data, error_response = validate_token_and_get_user(request, error_status_code=True)
            if error_response:
                return error_response

            # 🔍 Call Django's built-in logout
            logout(request)

            # 🗑 Delete the token to invalidate future access
            token.delete()

            return JsonResponse({
                "status": "logged_out",
                "message": "Logout successful"
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
