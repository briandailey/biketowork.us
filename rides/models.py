from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    user = models.ForeignKey(User)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def minutes(self):
        return round((self.end_time - self.start_time).seconds/60.0)

    def __str__(self):
        return "{minutes}m, {distance} miles by {user}".format(
                minutes=self.minutes,
                distance=self.distance,
                user=self.user)


