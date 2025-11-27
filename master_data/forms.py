from django import forms
from .models import EventType


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['event_type']
        widgets = {
            'event_type': forms.TextInput(attrs={'class': 'form-control'}),
        }
