from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'metube.views.home', name='home'),
    url(r'^facebook_crawler/', include('metube.fb_crawler.urls')),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout'),
)
