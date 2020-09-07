from datetime import timedelta

from django.utils import timezone
from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .views import EventListView, EventDetailView
from .models import Event


class TestEvent(TestCase):
    def setUp(self):
        self.organizer = User.objects.create(
            username='organizer',
            password='supersecure',
        )
        self.attendee = User.objects.create(
            username='attendee',
            password='verysafe',
        )
        self.organizer.is_active = True
        self.organizer.save()
        self.attendee.is_active = True
        self.attendee.save()
        self.test_event = Event.objects.create(
            name='Test Event',
            venue='London',
            organizer=self.organizer,
            date=timezone.now() + timedelta(days=10),
            capacity=1
        )

    def test_event_str(self):
        self.assertEqual(str(self.test_event), 'Test Event')

    def test_is_fully_booked(self):
        self.assertFalse(self.test_event.is_fully_booked)

        self.test_event.attendees.add(self.attendee)
        self.assertTrue(self.test_event.is_fully_booked)


class TestEventUrls(SimpleTestCase):
    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, EventListView)

    def test_event_detail_url(self):
        url = reverse('event-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, EventDetailView)
