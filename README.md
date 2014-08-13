### What Is Django?

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
  - Use virtualenv and virtualenvwrapper (why?)
  - Set up a requirements.txt (why?)

### Project Requirements

- Let's build a project!
  - An app that I can log my bike rides to work.
  - For now, I simply want to record total ride time and distance.

### Starting a Django Project

- A project contains multiple applications.

```
mkvirtualenv biketowork
pip install django
django-admin.py startproject biketowork
cd biketowork
./manage.py runserver
```

- oh look, a webserver that already works!

### Creating an App

- Ok, time to create ourselves a "ride". where's our models file?
- Models belong to apps. we have a project, but no apps yet.

```
./manage.py startapp rides
```

- Why did we use a pluralized word here? no particular reason, but it is more or less conventional practice.
- Now we have something that looks like this:

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

### Creating a Model

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

### Admin Management

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


### Creating Views


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

- look at that! it's just a regex! pretty simple, right?
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

### Creating Templates

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

- Alright! Now how do we show that variable inside the template?
    - what you need to know about templates...
    - variables are printed out with ```{{ variable }}```
    - some control logic (but no much) can be wrapped in ```{% if this %} {% endif %}```
    - if you came from PHP or Ruby, be aware that templates are weak for building business logic for a reason.
        - From the Django overlords: "_the template system is meant to express presentation, not program logic._."
        - the template language does not mix Python with HTML.
    - filters allow you to modify how variables are displayed, but they can also be abused to create your own filters that handle business logic
        - using filters to perform business logic is generally a bad idea; keep that in your views.
    - an example of a filter would be ```{{ variable|default:"nothing here" }}```
        - the default filter takes a None value and replaces it with the "nothing here" string.
- let's go ahead and use a for loop to iterate over each of our rides and display them.

```
  {% for ride in rides %}
    {{ ride }}
    <br/>
  {% endfor %}
```

- hooray! it's quite simple, but it does show our rides.
- there is another way to accomplish this, using class-based views.
    - not going to really cover that as I'm not really a big fan of them.
    - however, for simple lists and updates, they can be convenient so you should familiarize yourself with them.
- how would we accommodate static files (JS and CSS)?
    - during development, we can use django.contrib.staticfiles to serve static content.
    - to do this, we need to make sure:
        - it's addded to settings.py,
        - we put our files somewhere Django can find them (or tell Django explicitly)
        - preferably, use the static template tag: ```{% load staticfiles %}```
            - this format allows you to include additional libraries in your templates.
- so in 2034670 we added the necessary settings and template tags to include the bootstap CSS file
- let's talk about the pattern of using a base html file and including small snippets inside it
    - this is a php common to php and ruby frameworks
    - keeps you from having to repeat the same html code (e.g., menus, css, js) in multiple places.
    - in 08869a2 we create a base template and inherit it from the recent ride template using ```{% extends %}``` and ```{% block %}```
    - you can have multiple blocks in a page.
        - common pattern is to have one for the header, footer, etc. anywhere you want to override the default.
- all we have for now is a single page listing rides.

### Adding User Authentication

- new requirement: I'd like to have the ability to have my friends add rides, too.
- for this, we'll need to:
    - accommodate the creation of user accounts
    - set up pages for users to manage their rides
    - create a leaderboard for rides in the past week
    - we'll use the new [django migrations](https://docs.djangoproject.com/en/dev/topics/migrations/) to modify our rides table to accommodate users.
- we can use the [stock authentication views](https://docs.djangoproject.com/en/1.7/topics/auth/default/#module-django.contrib.auth.views) initially
    - the login template by default is ```registration/login.html```
    - we could create the form with a simple {{ form }} tag
    - however, the django default is to create an html table.
    - we could break each form field into fields, but that is laborious at best.
    - let's not reinvent the wheel - let's install django-bootstrap-form
    - this is one of the nice things about django - somebody has probably already done what you need
        - just ```pip install django-bootstrap-form```
    - add the app to the settings, load the template tag, and now you can use {{ form|bootstrap }} (40d2540)
    - we need to update settings to redirect the user to the proper place on login, rather than the default /account/profile (d49244d)
    - let's add the user name to the base template (24b0367)
    - note that the user name doesn't show up in the "recent" page.
    - this is because the user variable isn't actually passed to the template
    - what if we wanted the user variable to be passed to every single template by default?
    - in that case, we would create a [context processor](https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors)
        - simple a method that accepts an HttpRequest object and returns a dictionary that will be added to the template context.
    - you would add that context processor to the list of TEMPLATE_CONTEXT_PROCESSORS in your settings
    - however, in this case, our work is already done.
        - TEMPLATE_CONTEXT_PROCESSORS already contains [the auth context processor](https://docs.djangoproject.com/en/dev/ref/templates/api/#django-contrib-auth-context-processors-auth) which contains the user and perms variables.
        - if we look at the [render_to_response](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#render-to-response) shortcut method, we can pass a context instance along with our variables.
        - or we can just the [render](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#django.shortcuts.render) method, which passes it automatically
            - just need to add the request object to the parameters (68d20ec)
    - reload, and there it is!

### Creating Migrations

- so far, however, our rides are not tied to any particular user.
    - we need to set up a foreign relationship to the Django User model.
        - django.contrib.auth.models.User
    - in this case, we want a many-to-one relationship (a user can have many rides)
    - that is a [ForeignKey](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey) relationship
    - there are other kinds of relationships, too.
        - [ManyToManyField](https://docs.djangoproject.com/en/dev/ref/models/fields/#manytomanyfield)
        - [OneToOneField](https://docs.djangoproject.com/en/dev/ref/models/fields/#onetoonefield)

```python
class Ride(models.Model):
    user = models.ForeignKey(User)
```

- Now, however, we need to reflect this change in the database.
    - Prior to Django 1.7, we would use ```./manage.py syncdb``` to re-create the table
        - this, however, was terribly inconvenient if you wanted to simply alter an existing table.
    - Django 1.7 now includes database migrations.
    - we can create a new migration by using ```./manage.py makemigrations```

```
./manage.py makemigrations
You are trying to add a non-nullable field 'user' to ride without a default;
we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime module is available, so you can do e.g. datetime.date.today()
>>> 1
Migrations for 'rides':
  0002_ride_user.py:
    - Add field user to ride
```

- now we just apply the migration:: ```./manage.py migrate```
- if we look at the Ride table, we can now see that the user column has been added.
- it even has a foreign key relationships built in (if your databse supports that)
- we can add the username to the ride information (__str__ method) (ee9e4cf)


### Testing Your Application

- Django also has a built-in framework for building tests.
- Let's add a test that confirms that the username is included in the Ride __str__ output.
    - we create a class in ```rides/test.py``` that inherits ```django.test.TestCase```
    - django TestCase is a subclass of unittest.TestCase, but it also comes with
        - automatic loading of fixtures
        - wraps each test in a database transaction
        - crease a TestClient instance (for testing request/response)
        - includes Django-specific assertions for testing for things like redirection and form errors
- we could create a Ride fixture, but in this test let's just create a setUp method that creates a ride (615dbf2)
- We'll create a method that confirms that the username is present in the output (db0d753)
- Now let's create another test, but instead of re-creating the object.create, let's refactor to use fixtures.
- You can use the ```./manage.py dumpdata``` command to dump specific models or app data for testing

```
./manage.py dumpdata rides --indent=4 > rides/fixtures/rides.json
./manage.py dumpdata auth --indent=4 > rides/fixtures/users.json
```

- Refactor to indicate which fixtures to load for the test. (4f4c74a)
- Now we can add another test for the recent view with similar data
    - we can use the [test client](https://docs.djangoproject.com/en/dev/topics/testing/tools/#the-test-client) to simulate web requests
    - test that the recent page has a 'login' link (976cda4)
    - test that if a user is logged in, the logout link is available (b1317e8).

### User Forms

- For now, the only way to create a ride is to do it via the Admin page.
    - If we log in as the test user, we can't create a ride!
    - only User.is_staff is allowed to access the /admin/ area.
    - We need a way for our friends to add new rides.
- We could write the form from scratch, but of course we don't have to...
- We can use [Django forms](https://docs.djangoproject.com/en/dev/topics/forms/)!
- For this simple form, let's use a Django [ModelForm](https://docs.djangoproject.com/en/dev/topics/forms/modelforms/) (16ae607).
- Add our view method, our template, and our URL route.
    - Note we used the bootstrap template filter again.
    - For now, the form is pretty basic. Date input is not terribly user friendly.

```python
from django.forms import ModelForm

from rides.models import Ride

class RideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['start_time', 'end_time', 'distance']
```

- and in view.py:

```python
def new(request):
    if request.method == 'GET':
        form = RideForm()
    else:   # request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'rides/new.html', {
            'form': form,
    })
```

- If you save this, it will complain that user_id is null.
- We need to set the user based on the session
    - which means that we should also require that the user log in!
    - for this we can use the @login_required decorator. (6c66db2)
- We can use the ModelForm instance keyword argument to provide the default user (65125a0).

```python
form = RideForm(request.POST, instance=Ride(user=request.user))
```

- Great! But now when we save it, it just shows the form with the same data.
- the Django [messages framework](https://docs.djangoproject.com/en/dev/ref/contrib/messages/) should help us out here!
- We need to add the message to the view, and then make sure we display messages in the base template (feda13c)

### Bells & Whistles

- We can do a few more things to make it a little nicer.
    - Show a link to the 'new' page (17689e5)
    - Use django.contrib.humanize to put a nice timestamp on recent rides (781976c)

### Production Deployment Patterns

- Now that we have an app, how would we host it?
    - There are PaaS companies like Heroku and Gondor that make it very easy.
    - However, assuming we have our own server...
- Common pattern is nginx + gunicorn.
- nginx serves up static files, plus a proxy off to gunicorn running on a Unix web socket.
- we need to communicate dependencies. pip and virtualenv make this quite easy.

```
pip freeze > requirements.txt
```

- this tells us what packages we need to run the application. we can install them in other environments with:

```
pip install -r requirements.txt
```

#### Rough draft area...

- how would we serve that up in a production environment? ([wsgi](http://legacy.python.org/dev/peps/pep-3333/#original-rationale-and-goals-from-pep-333))
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
