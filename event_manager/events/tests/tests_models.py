from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Event


class TestEventModels(TestCase):
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
            date=date.today() + timedelta(days=10),
            capacity=1
        )

    def test_event_str(self):
        self.assertEqual(str(self.test_event), 'Test Event')

    def test_is_fully_booked(self):
        self.assertFalse(self.test_event.is_fully_booked)

        self.test_event.attendees.add(self.attendee)
        self.assertTrue(self.test_event.is_fully_booked)