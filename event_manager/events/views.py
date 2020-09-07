from datetime import date, timedelta

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Event


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


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'description', 'date', 'venue', 'capacity']

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        if form.instance.date < date.today() + timedelta(days=1):
            msg = messages.error(self.request, f'Cannot schedule events in the past or today!')
            return super().form_invalid(form)
        return super().form_valid(form)