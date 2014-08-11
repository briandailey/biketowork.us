from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from rides.models import Ride


class TestRide(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='test',
            password='test',
            email='test@dailytechnology.net',
        )
        Ride.objects.create(
            user=user,
            distance=5.5,
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + timedelta(hours=1.5)
        )
