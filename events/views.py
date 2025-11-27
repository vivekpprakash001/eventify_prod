from django.views import generic
from django.urls import reverse_lazy
from .models import Event
from .models import EventImages
from .forms import EventForm
from .forms import EventImagesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/event_list.html'
    paginate_by = 10


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')


@login_required
def add_event_images(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        form = EventImagesForm(request.POST, request.FILES)

        images = request.FILES.getlist('event_image')

        if images:
            for img in images:
                EventImages.objects.create(event=event, event_image=img)

            messages.success(request, "Images uploaded successfully!")
            return redirect("events:event_images", pk=event.pk)

    else:
        form = EventImagesForm()

    return render(request, "events/event_images_form.html", {
        "form": form,
        "event": event,
    })


@login_required
def event_images(request, pk):
    event = get_object_or_404(Event, pk=pk)
    images = EventImages.objects.filter(event=event)
    return render(request, "events/event_images_list.html", {
        "event": event,
        "images": images,
    })


@login_required
def set_primary_image(request, pk, img_id):
    event = get_object_or_404(Event, pk=pk)

    EventImages.objects.filter(event=event, is_primary=True).update(is_primary=False)
    EventImages.objects.filter(pk=img_id).update(is_primary=True)

    messages.success(request, "Primary image updated!")
    return redirect("events:event_images", pk=pk)


@login_required
def delete_event_image(request, pk, img_id):
    image = get_object_or_404(EventImages, pk=img_id)
    image.delete()
    messages.success(request, "Image deleted!")
    return redirect("events:event_images", pk=pk)
