from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.views import serve
from metube.blog.models import Blog, BlogForm

def home(request):
	content = {}
	content["blog"] = Blog.objects.order_by("-date")[0]
	return render(request, "blog/blog.html", content)

def edit(request, pk):
	content = {}
	blog = Blog.objects.get(pk=pk)
	# POST
	if request.method == "POST":
		f = BlogForm(request.POST, instance=blog)
		if f.is_valid():
			f.save()
		else:
			content["blog_form"] = f
			return render(request, "blog/blog_edit.html", content)
		return HttpResponseRedirect(reverse("blog_home"))
	
	# GET
	content["blog"] = blog
	content["blog_form"] = BlogForm(instance=blog)
	return render(request, "blog/blog_form.html", content)

def show(request, slug):
	pass

def search_by_tag(request, tag):
	pass
