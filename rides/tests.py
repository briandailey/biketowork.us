from datetime import timedelta
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import User

from rides.models import Ride


class TestRide(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test',
            password='test',
            email='test@dailytechnology.net',
        )
        self.ride = Ride.objects.create(
            user=self.user,
            distance=5.5,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1.5)
        )

    def test_user_in_ride_description(self):
        self.assertTrue(self.user.username in str(self.ride))
