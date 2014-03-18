from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.views import serve
from metube.blog.models import Blog, BlogForm

def home(request):
	content = {}
	content["blog"] = Blog.objects.order_by("-date")[0]
	return render(request, "blog/blog.html", content)

@permission_required("blog.change")
def edit(request, pk):
	content = {}
	blog = Blog.objects.get(pk=pk)
	content["existing_blog"] = True
	content["blog_id"] = pk
	# POST
	if request.method == "POST":
		f = BlogForm(request.POST, instance=blog)
		if f.is_valid():
			f.save()
		else:
			content["blog_form"] = f
			return render(request, "blog/blog_form.html", content)
		return HttpResponseRedirect(reverse("blog_show", args=(blog.slug,)))
	
	# GET
	content["blog_form"] = BlogForm(instance=blog)
	return render(request, "blog/blog_form.html", content)

@permission_required("blog.add")
def new(request):
	content = {}
	# POST
	if request.method == "POST":
		f = BlogForm(request.POST)
		if f.is_valid():
			blog = f.save()
		else:
			content["blog_form"] = f
			return render(request, "blog/blog_form.html", content)
		return HttpResponseRedirect(reverse("blog_show", args=(blog.slug,)))
	
	# GET
	content["blog_form"] = BlogForm()
	return render(request, "blog/blog_form.html", content)

def show(request, slug):
	content = {}
	#content["blog"] = Blog.objects.get(slug=slug)
	#return render(request, "blog/blog.html", content)
	content["blog"] = Blog.objects.order_by("-date")[0]
	return render(request, "blog/blog.html", content)

def tag(request, tag):
	pass
