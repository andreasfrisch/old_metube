from django.conf.urls import patterns, include, url

urlpatterns = patterns('metube.blog.views',
    url(r'^$', 'home', name='blog_home'),
    url(r'edit/(?P<pk>\w+)$', 'edit', name='blog_edit'),
    url(r'new$', 'new', name='blog_new'),
    url(r'slug/(?P<slug>[-\w]+)$','show',name='blog_show'),
    url(r'tag/(?P<tag>[-\w]+)$', 'tag', name='blog_tag'),
    url(r'archive$', 'archive', name='blog_archive'),
)
