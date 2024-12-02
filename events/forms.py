from django.utils import timezone
from django import forms
from django.forms import ModelForm, ValidationError
from events.models import Events
from django.utils.html import strip_tags

class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "description", "start_date", "end_date", "location", "promotion_type"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name of event'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the event'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location of event'
            }),
            'promotion_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter type of promotion'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        today = timezone.localdate()  

        if end_date and end_date < today:
            self.add_error('end_date', 'The end date cannot be in the past. Please enter a date that is today or in the future.')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('start_date', 'The start date cannot be after the end date. Please enter a start date that is before the end date.')

        # Strip tags from other inputs to prevent XSS
        for field in ['name', 'description', 'location', 'promotion_type']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])

        return cleaned_data