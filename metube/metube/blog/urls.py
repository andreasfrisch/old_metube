from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# list all blogs
    url(
    		r'^$',
    		'metube.blog.views.home',
    		name='blog_home'
    ),
	# edit specific post
    url(
    		r'edit/(?P<pk>\w+)$',
    		'metube.blog.views.edit',
    		name='blog_edit'
    ),
	# show specific post
    url(
    		r'slug/(?P<slug>\w+)$',
    		'metube.blog.views.show',
    		name='blog_show'
    ),
	# search by tag
    url(
    		r'search_by_tag/(?P<tag>\w+)$',
    		'metube.blog.views.search_by_tag',
    		name='blog_search_by_tag'
    ),
)
