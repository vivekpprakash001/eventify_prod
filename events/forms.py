from django import forms
from .models import Event
from .models import EventImages


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'important_information': forms.Textarea(attrs={'class': 'form-control'}),
            'venue_name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'outside_event_url': forms.URLInput(attrs={'class': 'form-control'}),
            'event_status': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'cancelled_reason': forms.Textarea(attrs={'class': 'form-control'}),
            'is_bookable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_eventify_event': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class EventImagesForm(forms.ModelForm):
    event_image = forms.ImageField(
        widget=MultipleFileInput(
            attrs={
                'multiple': True,
                'class': 'form-control',
            }
        ),
        label="Upload Images"
    )

    class Meta:
        model = EventImages
        fields = ['event_image', 'is_primary']
        widgets = {
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_primary': 'Set as Primary Image (If only one uploaded)',
        }
