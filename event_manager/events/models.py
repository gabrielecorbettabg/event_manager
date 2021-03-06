from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Event(models.Model):
    """
    Handle event objects.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    date = models.DateField()
    venue = models.TextField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attendees_set', blank=True)
    capacity = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.name

    @property
    def is_fully_booked(self):
        if len(self.attendees.all()) < self.capacity:
            return False
        return True

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
