from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        form = RideForm(request.POST, instance=Ride(user=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Ride recorded!')
            return redirect('recent_rides')
    # messages? # validation? etc
    return render(request, 'rides/new.html', {
            'form': form,
    })
