from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('WeatherAPI.WeatherGrab.views',
    # Examples:
    # url(r'^$', 'WeatherAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'getweatherdetails'),
    url(r'^admin/', include(admin.site.urls)),
)
