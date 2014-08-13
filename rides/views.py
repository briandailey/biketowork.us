from django.shortcuts import render, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required

# because the models are in the same module, we can use a relative import here.
from .models import Ride
from .forms import RideForm

def recent(request):
    rides = Ride.objects.order_by('-start_time')[:5]
    return render(request, 'rides/recent.html', {
            'rides': rides,
    })

@login_required
def new(request):
    if request.method == 'GET':
        form = RideForm()
    else:   # request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            form.save()
    # messages? # validation? etc
    return render(request, 'rides/new.html', {
            'form': form,
    })
