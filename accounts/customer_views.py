
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .customer_forms import RegisterForm
from .customer_forms import CustomerLoginForm
from .customer_forms import CustomerProfileForm

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from master_data.models import EventType
from events.models import Event

from django.db.models import Prefetch
from events.models import EventImages

from django.forms.models import model_to_dict
# from utils.date_convertor import convert_date_to_dd_mm_yyyy

def send_verification_email(request, user):
    """
    Renders and sends verification email with activation link.
    Requires EMAIL_BACKEND configured.
    """
    current_site = get_current_site(request)
    subject = "Verify your email for {}".format(current_site.name)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activate_path = reverse_lazy('accounts:login', kwargs={'uidb64': uid, 'token': token})
    activate_url = request.build_absolute_uri(activate_path)
    message = render_to_string('auth/email_verification_email.txt', {
        'user': user,
        'activate_url': activate_url,
        'domain': current_site.domain,
    })
    user.email_user(subject, message)


class RegisterView(FormView):
    template_name = "customer/customer_registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # send_verification_email(self.request, user)
        messages.success(self.request, "Account created. Kindly login to continue.")
        return super().form_valid(form)


class EmailVerificationSentView(View):
    template_name = "auth/email_verification.html"

    def get(self, request):
        return render(request, self.template_name)


class ActivateAccountView(View):
    """
    Activation link view: sets user.is_active=True if token valid.
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verified — you can now sign in.")
            return redirect('login')
        else:
            return render(request, 'auth/activation_invalid.html')


def login_view(request):
    if request.method == "POST":
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('customer_dashboard')
    else:
        form = CustomerLoginForm(request)
    return render(request, 'customer/customer_login.html', {'form': form})

@login_required(login_url="login")
def customer_dashboard(request):
    event_types = EventType.objects.all()

    events = Event.objects.all()
    
    events_dict = [model_to_dict(obj) for obj in events]

    for event in events_dict:
        try:
            image = EventImages.objects.get(event=event['id'], is_primary=True).event_image.url
            event['event_image'] = image
        except Exception as e:
            event['event_image'] = ''
        # event['start_date'] = convert_date_to_dd_mm_yyyy(event['start_date'])

    context = {
        'event_types': event_types,
        'events': events_dict,
    }
    return render(request, "customer/customer_dashboard.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required(login_url="login")
def customer_calendar(request):
    return render(request, "customer/customer_calendar.html")



# ...existing imports...

@login_required(login_url="login")
def customer_profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("customer_profile")
    else:
        form = CustomerProfileForm(instance=user)

    return render(request, "customer/customer_profile.html", {"form": form})