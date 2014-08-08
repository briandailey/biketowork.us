from django.shortcuts import render, render_to_response, HttpResponse

# because the models are in the same module, we can use a relative import here.
from .models import Ride

def recent(request):
    rides = Ride.objects.order_by('-start_time')[:5]
    return render_to_response('rides/recent.html', {
        'rides': rides,
    })
