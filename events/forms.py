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
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_start_date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_end_date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_start_time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_end_time'}),
            'all_year_event': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_all_year_event'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if all_year_event is True (from instance or initial data)
        all_year_event = False
        if self.instance and self.instance.pk:
            all_year_event = self.instance.all_year_event
        elif 'all_year_event' in self.initial:
            all_year_event = self.initial['all_year_event']
        elif self.data and 'all_year_event' in self.data:
            all_year_event = self.data.get('all_year_event') == 'on' or self.data.get('all_year_event') == 'True'
        
        # If all_year_event is True, disable date/time fields
        if all_year_event:
            self.fields['start_date'].widget.attrs['disabled'] = True
            self.fields['end_date'].widget.attrs['disabled'] = True
            self.fields['start_time'].widget.attrs['disabled'] = True
            self.fields['end_time'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        all_year_event = cleaned_data.get('all_year_event', False)
        
        # If all_year_event is True, clear date/time fields
        if all_year_event:
            cleaned_data['start_date'] = None
            cleaned_data['end_date'] = None
            cleaned_data['start_time'] = None
            cleaned_data['end_time'] = None
        
        return cleaned_data


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
