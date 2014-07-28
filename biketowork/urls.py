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
