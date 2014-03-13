from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'metube.project_tracker.views.home', name='tracker_home'),
)
