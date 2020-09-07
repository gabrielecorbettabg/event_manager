from datetime import date, timedelta

from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .views import EventListView, EventDetailView, EventCreateView
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
            date=date.today() + timedelta(days=10),
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

    def test_event_create_url(self):
        url = reverse('event-create')
        self.assertEqual(resolve(url).func.view_class, EventCreateView)


class TestEventViews(TestCase):
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
            id=1,
            name='Test Event',
            venue='London',
            organizer=self.organizer,
            date=date.today() + timedelta(days=10),
            capacity=1
        )
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/home.html')
        self.assertEqual(len(response.context['events']), 1)

    def test_event_detail_view(self):
        response = self.client.get(reverse('event-detail', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertEqual(response.context['event'].name, 'Test Event')

    def test_event_create_view(self):
        response = self.client.get(reverse('event-create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_event_create_valid(self):
        self.client.force_login(self.organizer)
        event_data = {
            'name': 'Aperitivo',
            'venue': 'Beach Bar',
            'capacity': 10,
            'date': date.today() + timedelta(days=5),
        }
        response = self.client.post(reverse('event-create'), event_data)
        self.assertEqual(response.status_code, 302)
        event_created = Event.objects.filter(name='Aperitivo').exists()
        self.assertTrue(event_created)

    def test_event_create_invalid(self):
        self.client.force_login(self.organizer)
        event_data = {
            'name': 'Aperitivo2',
        }
        response = self.client.post(reverse('event-create'), event_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        event_created = Event.objects.filter(name='Aperitivo2').exists()
        self.assertFalse(event_created)
