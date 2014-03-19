from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.views import serve
from metube.blog.models import Blog, BlogForm, Tag

def home(request):
	content = {}
	slug = Blog.objects.order_by("-date")[0].slug
	return HttpResponseRedirect(reverse("blog_show", args=(slug,)))

@permission_required("blog.change")
def edit(request, pk):
	content = {}
	blog = Blog.objects.get(pk=pk)
	content["existing_blog"] = True
	content["blog_id"] = pk
	content["tags"] = Tag.objects.all()
	# POST
	if request.method == "POST":
		f = BlogForm(request.POST, instance=blog)
		if f.is_valid():
			f.save()
		else:
			content["blog_form"] = f
			return render(request, "blog/form.html", content)
		return HttpResponseRedirect(reverse("blog_show", args=(blog.slug,)))
	
	# GET
	content["blog_form"] = BlogForm(instance=blog)
	return render(request, "blog/form.html", content)

@permission_required("blog.add")
def new(request):
	content = {}
	content["tags"] = Tag.objects.all()
	# POST
	if request.method == "POST":
		f = BlogForm(request.POST)
		if f.is_valid():
			blog = f.save()
		else:
			content["blog_form"] = f
			return render(request, "blog/form.html", content)
		return HttpResponseRedirect(reverse("blog_show", args=(blog.slug,)))
	
	# GET
	content["blog_form"] = BlogForm()
	return render(request, "blog/form.html", content)

def show(request, slug):
	content = {}
	blog = get_object_or_404(Blog, slug=slug)
	content["blog"] = blog
	content["tags"] = Tag.objects.all()
	return render(request, "blog/blog.html", content)

def tag(request, tag):
	content = {}
	content["blogs"] = Blog.objects.filter(tags__title=tag)
	content["tags"] = Tag.objects.all()
	return render(request, "blog/list.html", content)

def archive(request):
	content = {}
	content["blogs"] = Blog.objects.all()
	content["tags"] = Tag.objects.all()
	return render(request, "blog/list.html", content)
