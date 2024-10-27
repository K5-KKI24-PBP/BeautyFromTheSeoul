from django import forms
from django.forms import ModelForm
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

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)
    
    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]
        return strip_tags(start_date)
    
    def clean_end_date(self):
        end_date = self.cleaned_data["end_date"]
        return strip_tags(end_date)
    
    def clean_location(self):
        location = self.cleaned_data["location"]
        return strip_tags(location)
    
    def clean_promotion_type(self):
        promotion_type = self.cleaned_data["promotion_type"]
        return strip_tags(promotion_type)