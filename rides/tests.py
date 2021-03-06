from datetime import timedelta
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import User

from rides.models import Ride


class TestRide(TestCase):
    fixtures = ['users', 'rides']

    def test_user_in_ride_description(self):
        ride = Ride.objects.all()[0]
        self.assertTrue(ride.user.username in str(ride))

class TestRecentRides(TestCase):
    fixtures = ['users', 'rides']

    def test_recent_rides_has_login_link(self):
        response = self.client.get('/')
        self.assertContains(response, 'login')

    def test_recent_rides_has_logout_link(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertContains(response, 'logout')
        self.assertNotContains(response, 'login')
