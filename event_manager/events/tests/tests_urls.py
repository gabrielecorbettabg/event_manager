from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, attend_event


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

    def test_event_update_url(self):
        url = reverse('event-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, EventUpdateView)

    def test_event_delete_url(self):
        url = reverse('event-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, EventDeleteView)

    def test_event_attend_url(self):
        url = reverse('event-attend', args=[1])
        self.assertEqual(resolve(url).func, attend_event)
