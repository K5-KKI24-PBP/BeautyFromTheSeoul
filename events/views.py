from functools import wraps
from django.shortcuts import render, redirect
from events.models import Events
from events.forms import EventsForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied. You must be a superuser to access this page.")
    return _wrapped_view

def show_events(request):
    events = Events.objects.all()
    context = {
        'events': events
    }
    return render(request, 'show_event.html', context)

@superuser_required
@login_required(login_url='authentication:login')
def create_event(request):
    user = request.user

    if user.is_superuser:
        if request.method == 'POST':
            form = EventsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('events:event')
        else:
            form = EventsForm()
    else:
        return HttpResponse("You are not authorized to create events.")
    
    context = {
        'form': form
    }
    return render(request, 'create_event.html', context)

@superuser_required
@login_required(login_url='authentication:login')
def edit_event(request, id):
    user = request.user

    if user.is_superuser:
        event = Events.objects.get(id=id)
        if request.method == 'POST':
            form = EventsForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('events:event')
        else:
            form = EventsForm(instance=event)
    else:
        return HttpResponse("You are not authorized to edit events.")

    context = {
        'form': form
    }
    return render(request, 'edit_event.html', context)

@superuser_required
@login_required(login_url='authentication:login')
def delete_event(request, id):
    user =  request.user

    if user.is_superuser:
        event = Events.objects.get(id=id)
        event.delete()
    else:
        return HttpResponse("You are not authorized to delete events.")
        
    return redirect('events:event')

def rsvp_event(request, id):
    # TODO: Implement RSVP events for user
    pass

def show_rsvp(request):
    # TODO: Implement shows the events card with rsvp button (for user)
    pass 
