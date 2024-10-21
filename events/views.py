from django.shortcuts import render, redirect
from events.models import Events
from events.forms import EventsForm

def show_events(request):
    events = Events.objects.all()
    context = {
        'events': events
    }
    return render(request, 'show_event.html', context)

def create_event(request):
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event')
    else:
        form = EventsForm()
    context = {
        'form': form
    }
    return render(request, 'create_event.html', context)
