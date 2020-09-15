from datetime import date, timedelta

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Event


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

    def test_organizer_view(self):
        self.client.force_login(self.attendee)
        response = self.client.get(reverse('my-events'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_organizer.html')
        self.assertEqual(len(response.context['events']), 0)

    def test_event_detail_view(self):
        response = self.client.get(reverse('event-detail', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertEqual(response.context['event'].name, 'Test Event')

    def test_event_create_view_unauthenticated_redirects_home(self):
        response = self.client.get(reverse('event-create'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/event/create/')

    def test_event_update_view_unauthenticated_redirects_home(self):
        response = self.client.get(reverse('event-update', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/event/1/update/')

    def test_event_delete_view_unauthenticated_redirects_home(self):
        response = self.client.get(reverse('event-delete', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/event/1/delete/')

    def test_event_attend_view_unauthenticated_redirects_home(self):
        response = self.client.get(reverse('event-attend', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/event/1/attend/')

    def test_event_create_view_authenticated(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_event_update_view_authenticated(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-update', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_event_delete_view_authenticated(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-delete', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_confirm_delete.html')

    def test_event_update_view_authenticated(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-update', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_event_delete_view_authenticated(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-delete', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_confirm_delete.html')

    def test_event_attend_view_GET(self):
        self.client.force_login(self.organizer)
        response = self.client.get(reverse('event-attend', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_attend.html')

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

    def test_invalid_past_event_create(self):
        self.client.force_login(self.organizer)
        event_data = {
            'name': 'Past event',
            'venue': '25 Queen Road',
            'capacity': 2,
            'date': date.today() - timedelta(days=4)
        }
        response = self.client.post(reverse('event-create'), event_data)
        msg = list(response.context.get('messages'))[0]
        self.assertEquals(msg.tags, 'error')
        self.assertEquals(msg.message, 'Cannot create events in the past or today!')
        event = Event.objects.filter(name='Past event').exists()
        self.assertFalse(event)

    def test_event_update_valid(self):
        self.client.force_login(self.organizer)
        event_data = {
            'name': 'Updated Test Event',
            'venue': '199 Power road',
            'capacity': 22,
            'date': date.today() + timedelta(days=15),
        }
        response = self.client.post(reverse('event-update', args=[self.test_event.id]), event_data)
        self.assertEqual(response.status_code, 302)
        event = Event.objects.get(pk=self.test_event.id)
        self.assertEqual(event.name, event_data['name'])
        self.assertEqual(event.venue, event_data['venue'])
        self.assertEqual(event.capacity, event_data['capacity'])
        self.assertEqual(event.date, event_data['date'])

    def test_event_update_invalid(self):
        self.client.force_login(self.organizer)
        event_data = {
            'venue': '199 Power road',
            'capacity': 52,
            'date': date.today() + timedelta(days=25),
        }
        response = self.client.post(reverse('event-update', args=[self.test_event.id]), event_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        event = Event.objects.get(pk=self.test_event.id)
        self.assertNotEqual(event.name, event_data['venue'])
        self.assertNotEqual(event.name, event_data['capacity'])
        self.assertNotEqual(event.name, event_data['date'])

    def test_invalid_past_event_update(self):
        self.client.force_login(self.organizer)
        event_data = {
            'name': 'Past Test event',
            'venue': '5 Queen Road',
            'capacity': 11,
            'date': date.today() - timedelta(days=4)
        }
        response = self.client.post(reverse('event-update', args=[self.test_event.id]), event_data)
        msg = list(response.context.get('messages'))[0]
        self.assertEquals(msg.tags, 'error')
        self.assertEquals(msg.message, 'Cannot schedule events in the past or today!')
        event = Event.objects.get(pk=self.test_event.id)
        self.assertNotEqual(event.name, event_data['name'])
        self.assertNotEqual(event.name, event_data['venue'])
        self.assertNotEqual(event.name, event_data['capacity'])
        self.assertNotEqual(event.name, event_data['date'])

    def test_unauthorized_event_update(self):
        self.client.force_login(self.attendee)
        event = Event.objects.get(pk=self.test_event.id)
        event_data = {
            'name': 'Should not update',
            'venue': event.venue,
            'capacity': event.capacity,
            'date': event.date
        }
        response = self.client.post(reverse('event-update', args=[self.test_event.id]), event_data)
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_event_delete(self):
        self.client.force_login(self.attendee)
        response = self.client.post(reverse('event-delete', args=[self.test_event.id]))
        self.assertEqual(response.status_code, 403)

    def test_success_event_delete(self):
        self.client.force_login(self.organizer)
        response = self.client.post(reverse('event-delete', args=[self.test_event.id]))
        self.assertEqual(response.status_code, 302)
        event = Event.objects.filter(pk=self.test_event.id).exists()
        self.assertFalse(event)

    def test_event_attend(self):
        self.client.force_login(self.organizer)
        self.client.post(reverse('event-attend', args=[self.test_event.id]))
        event_updated = Event.objects.get(pk=self.test_event.id)
        self.assertEqual(event_updated.attendees.all().count(), 1)

        self.client.force_login(self.attendee)
        self.client.post(reverse('event-attend', args=[self.test_event.id]))
        event_updated = Event.objects.get(pk=self.test_event.id)
        self.assertEqual(event_updated.attendees.all().count(), 1)
