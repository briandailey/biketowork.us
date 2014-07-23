from django.db import models

class Ride(models.Model):
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return "{minutes}m, {distance} miles".format(
                minutes=round((self.start_time - self.end_time).seconds/60, 2),
                distance=self.distance)


