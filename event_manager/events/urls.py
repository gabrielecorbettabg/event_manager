from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView

urlpatterns = [
    path('', EventListView.as_view(), name='home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/create/', EventCreateView.as_view(), name='event-create')
]
