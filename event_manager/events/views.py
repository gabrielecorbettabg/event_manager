from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/home.html'
    context_object_name = 'events'
    ordering = ['date']


class EventDetailView(DetailView):
    model = Event


class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'description', 'date', 'venue', 'capacity']

    def form_valid(self, form):
        # set creating user as organizer
        form.instance.organizer = self.request.user
        return super().form_valid(form)