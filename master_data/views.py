from django.views import generic
from django.urls import reverse_lazy
from .models import EventType
from .forms import EventTypeForm
from django.contrib.auth.mixins import LoginRequiredMixin

class EventTypeListView(LoginRequiredMixin, generic.ListView):
    model = EventType
    template_name = 'master_data/event_type_list.html'
    context_object_name = 'categories'

class EventTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'master_data/event_type_form.html'
    success_url = reverse_lazy('master_data:event_type_list')

class EventTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'master_data/event_type_form.html'
    success_url = reverse_lazy('master_data:event_type_list')

class EventTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = EventType
    template_name = 'master_data/event_type_confirm_delete.html'
    success_url = reverse_lazy('master_data:event_type_list')
