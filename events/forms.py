from django.forms import ModelForm
from events.models import Events

class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "description", "start_date", "end_date", "location", "promotion_type"]