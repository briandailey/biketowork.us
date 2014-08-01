- What is Django?
  - A web framework
  - What is a web framework?
    - Library of tools for developing web applications
    - An abstraction of common web development approaches
  - MVT (not MVC)
    - Model the data (a SQL table)
    - View is the program logic
    - Template renders with populated data
  - What makes Django interesting?
    - One of the more popular Python web frameworks
      - Mozilla, Disqus, Pinterest, Instagram
      - Emma, Stratasan, Eventbrite
    - Gives you an automatic administration interface
    - Includes most of the batteries
      - User authentication
      - Smart security defaults
    - Documentation is really nice (both the online docs and built into the code)
- How to get it set up
  - Mac & Linux already have Python
  - Windows, use Portable Python 2.7
  - Use pip (why?)
  - Use virtualenv (why?)
  - Set up a requirements.txt (why?)
- The Almighty Request & Response
  - A step through the lifecycle
- Let's build a project!
  - An app that I can log my bike rides to work.
  - I want to record total ride time, distance, and show average speed.
- Explain project vs. app

```
mkvirtualenv biketowork
pip install django
django-admin.py startproject biketowork
cd biketowork
./manage.py runserver
```

- oh look, a webserver that already works!
- ok, time to create ourselves a "ride". where's our models file?
- models belong to apps. we have a project, but no apps yet.

```
./manage.py startapp rides
```

- why did we use a pluralized word here? no particular reason, but it is more or less conventional practice.
- now we have something that looks like this:

```
.
├── biketowork
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── rides
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── tests.
    └── views.py
```

- great! now we have a models file! let's create a ride model.
- we said we wanted to create a ride with distance and time.
- open up models.py and create one!
- we want to extend [models.Model](https://docs.djangoproject.com/en/1.6/topics/db/models/)
- distance should probably be numeric with a decimal. what [field types](https://docs.djangoproject.com/en/1.6/ref/models/fields/) are available?
  - how about [DecimalField](https://docs.djangoproject.com/en/1.6/ref/models/fields/#decimalfield)?
  - notice that required attributes for a DecimalField are max_digits and decimal_places
  - let's go with 5 maximum digits with 2 decimal places (think someone will go for a ride of > 999.99 miles?)
- time is a little trickier. how should we represent it? minutes? seconds? hours?
  - how about we just go with start time and end time? then we could chart when we ride.
  - we could use timefield, but that wouldn't include dates. datefield wouldn't inclue time.
  - aha! how about [DateTimeField](https://docs.djangoproject.com/en/1.6/ref/models/fields/#datetimefield)?
  - add a start time and an end time.

```python
class Ride(models.Model):
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
```

- now let's create a the database table.

```
./manage.py syncdb
./manage.py runserver
```

- still nothing on the web page, or at /admin/
- need to add the model to rides/admin.py
- open up rides/admin.py and add:

```python
from .models import Ride
admin.site.register(Ride)
```

- now you can [add a ride](http://localhost:8000/admin/rides/ride/add/).
- note how the admin has a fairly nice UI for adding rides - calendar for date/time, increment miles with arrows, etc.
- note how when you list the new rides it simply shows "ride object."
- the first thing we can do is return a usable string of text by overriding the __unicode__ method on the Ride model.

```python
    def __str__(self):
        return "{minutes}m, {distance} miles".format(
                minutes=round((self.start_time - self.end_time).seconds/60, 2),
                distance=self.distance)
```

- that now shows a little more information on the admin. but what about a table where we can see start, stop, and mileage and sort it?

```python
class RideAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'distance')

admin.site.register(Ride, RideAdmin)
```

- The ModelAdmin object has [many configurable options](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-options)
- We can even made a new model property (minutes) and show it on the admin page, too.
- The admin is extensible, theme-able, and easy to set up. However, you don't really want to use it for your entire site.
- What if we wanted the landing page to show us the five most recent rides?
    - To the view layer!
- views are the glue between the models and the templates
    - simply put, a view accepts a request and returns a response.
    - you can use a template to make things easier for you
        - think of a template as a static page with dynamic variables
    - but you don't have to use a template. you just have to return some kind of response.
- let's go ahead and create a really simple view

```python
from django.shortcuts import HttpResponse

def recent(request):
    return HttpResponse('leeeroy jenkins!')
```

- first, we need to tell django that the root url will point to a view method
    - urls are mapped in urls.py
    - there's a project urls.py, and an app urls.py
        - a common pattern is to set up most urls in the app and include them in the project
    - let's edit the project urls.py file for now

```python
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rides.views import recent

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'biketowork.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', recent),
)
```

- let's talk about querysets.
    - this is how we pull from the DB via the ORM, show it on the page.
        - what is an ORM?
        - basically creates an object-oriented model of the database row
        - the django model object also acts as a manager for querying the database for multiple objects
    - we said we wanted the five most recent rides. we have a ride object, how do we get many objects and iterate over them?
    - but the model manager is accessed via Model.objects, which allows us to talk to the DB.
    - For example, ```ride = Ride.objects.get(pk=1)``` would get the Ride object with a primary key of 1 and store it in the variable ```ride```
    - You can also grab multiple objects: ```rides = Ride.objects.filter(distance=1)```
    - filter is pretty powerful, and allows you to also do things like ```ride = Ride.objects.filter(distance__gte=4)```
    - you can sort the objects you search for: ```Ride.objects.order_by('start_time')```
    - you can also drop into raw SQL, or grab child and parent objects.
    - you can limit the results (with a SQL ```LIMIT```) by using python list syntax: ```Ride.objects.all()[:5])```
    - first, we need to import the Ride model into the view
    - Now, inside the view method, we create a variable for the rides
- before we pass the variable to a template, we need to create it!
    - before we create it, we have to tell our application where to look for templates.
    - this is defined in [settings.TEMPLATE_DIRS](https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs)
        - TEMPLATE_DIRS is simply a list of locations for django to look for templates.
        - in biketowork/settings.py...

```python
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)
```

- Now we can create the template file in BASE_DIR/templates/
    - in this case, templates/rides/recent.html
    - we'll create a basic HTML file for now.
- Then we can update the view and use [```render_to_response```](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#django.shortcuts.render_to_response)

```python
def recent(request):
    rides = Ride.objects.order_by('-start_time')[:5]
    return render_to_response('rides/recent.html', {
        'rides': rides,
    })
```


#### Rough draft area...

- show most recent five in templates, show how to render a template with variables
    - start with just render httpresponse
    - then actually populate variables in template, use render_to_response shortcut
    - show how to include logic, variables, and what filters are.
    - briefly talk about class-based views

- set up urls.py to show this new page at the root
    - it's just regex!
- ok, let's add a user account and authentication (how easy was that?)
    - maybe use an add-in for social account login?
    - demonstrate how you don't always need to recreate the wheel
    - add add-in to requirements.txt (what is requirements.txt?)
- create a base template that others extend
- demonstrate how to set up a relationship between objects
- now let's say we want to show per user, and change it
- demonstrate how we put variables in a url pattern (to change user)
- forms so non-admin can create a ride
- create a test



Resources:
http://www.slideshare.net/mpirnat/web-development-with-python-and-django
