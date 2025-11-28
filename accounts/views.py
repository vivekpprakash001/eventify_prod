from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import LoginForm
from .forms import UserForm
from events.models import Event
from master_data.models import EventType

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages


def dashboard(request):
    total_events = Event.objects.count()
    total_categories = EventType.objects.count()
    total_users = User.objects.count()
    return render(request, 'dashboard.html', {
        'total_events': total_events,
        'total_categories': total_categories,
        'total_users': total_users,
    })


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")  # Redirect authenticated user

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
