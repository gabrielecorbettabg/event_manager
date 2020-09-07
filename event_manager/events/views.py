from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "events/home.html"
    context_object_name = "events"
    ordering = ["date"]


class EventDetailView(DetailView):
    model = Event
