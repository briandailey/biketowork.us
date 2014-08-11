from django.forms import ModelForm

from rides.models import Ride

class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['start_time', 'end_time', 'distance']
