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

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
