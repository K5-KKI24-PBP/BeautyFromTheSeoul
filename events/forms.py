from django import forms
from django.forms import ModelForm
from events.models import Events

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
                'placeholder': 'YYYY-MM-DD'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'YYYY-MM-DD'
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