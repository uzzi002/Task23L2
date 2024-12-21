from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Event
from django.contrib.auth.decorators import login_required

def home(request):
    """Render the home page with login and register links."""
    return render(request, 'events/home.html')

def user_register(request):
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created! Please log in.")
            return redirect('events:login')
    return render(request, 'events/register.html')

def user_login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('events:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'events/login.html')

def user_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect('events:home')

@login_required
def dashboard(request):
    """Display all events."""
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/dashboard.html', {'events': events})

@login_required
def create_event(request):
    """Create a new event."""
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        location = request.POST['location']

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            organizer=request.user
        )
        messages.success(request, "Event created successfully!")
        return redirect('events:dashboard')

    return render(request, 'events/create_event.html')

@login_required
def edit_event(request, pk):
    """Edit an event."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.location = request.POST['location']
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect('events:dashboard')

    return render(request, 'events/edit_event.html', {'event': event})

@login_required
def delete_event(request, pk):
    """Delete an event."""
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('events:dashboard')
