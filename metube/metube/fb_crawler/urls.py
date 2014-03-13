from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# list all crawler requests
    url(
    		r'^$',
    		'metube.fb_crawler.views.view_all',
    		name='crawler_all'
    ),
	# new crawl request, GET presents form
    url(
    		r'new_request/$',
    		'metube.fb_crawler.views.new_crawl_request',
    		name='crawler_new'
    ),
	# serve file
    url(
    		r'get_file/(?P<filetype>\w+)/(?P<request_id>\d+)$',
    		'metube.fb_crawler.views.get_file',
    		name='crawler_get_file'
    ),
)
