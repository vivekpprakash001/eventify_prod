from django import forms
from .models import EventType


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['event_type', 'event_type_icon']
        widgets = {
            'event_type': forms.TextInput(attrs={'class': 'form-control'}), 
            'event_type_icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'event_type': 'Event Type',
            'event_type_icon': 'Event Type Icon',
        }
