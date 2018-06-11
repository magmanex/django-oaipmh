from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import ExampleOAIProvider


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_project.views.home', name='home'),
    # url(r'^example_project/', include('example_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^oai/', ExampleOAIProvider.as_view()),
)