from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserForm
from events.models import Event
from master_data.models import EventType

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
