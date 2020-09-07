from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import connection, IntegrityError

from .models import Event


@login_required
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_fully_booked:
        messages.error(request, f'Sorry, this event is fully booked')
        return render(request, 'events/event_attend.html', {'event': event})

    if request.method == 'POST':
        try:
            with connection.cursor() as cr:
                cr.execute("INSERT INTO events_event_attendees (event_id, user_id) VALUES (%s, %s)",
                           [pk, request.user.id])
            messages.success(request, f'You have successfully registered to {event.name}!')
            return redirect('home')
        # ToDo:Handle other exceptions
        except IntegrityError:
            messages.error(request, f'You are already registered to {event.name}!')

    return render(request, 'events/event_attend.html', {'event': event})


class EventListView(ListView):
    model = Event
    template_name = 'events/home.html'
    context_object_name = 'events'
    ordering = ['date']


class EventDetailView(DetailView):
    model = Event


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'description', 'date', 'venue', 'capacity']

    def form_valid(self, form):
        # set creating user as organizer
        form.instance.organizer = self.request.user
        if form.instance.date < date.today() + timedelta(days=1):
            msg = messages.error(self.request, f'Cannot create events in the past or today!')
            return super().form_invalid(form)
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['name', 'description', 'date', 'venue', 'capacity']

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        if form.instance.date < date.today() + timedelta(days=1):
            msg = messages.error(self.request, f'Cannot schedule events in the past or today!')
            return super().form_invalid(form)
        return super().form_valid(form)

    def test_func(self):
        if self.request.user == self.get_object().organizer:
            return True
        return False


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('home')

    def test_func(self):
        if self.request.user == self.get_object().organizer:
            return True
        return False


