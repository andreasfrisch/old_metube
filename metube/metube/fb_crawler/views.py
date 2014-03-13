import os
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.views import serve
from metube.settings import MEDIA_ROOT
from metube.fb_crawler.models import CrawlRequest, CrawlRequestForm
from metube.fb_crawler.crawler.request_manager import manage_requests

def view_all(request):
	content = {}
	content["crawl_requests"] = CrawlRequest.objects.all()
	return render(request, "fb_crawler/list.html", content)

def new_crawl_request(request):
	content = {}
	# POST
	if request.method == "POST":
		f = CrawlRequestForm(request.POST)
		if f.is_valid():
			instance = f.save(commit=False)
			instance.filename = "[%s_%s]_%s" % (
					f.cleaned_data["facebook_id"],
					f.cleaned_data["created_date"].strftime("%d-%m-%Y--%H:%M"),
					"-".join(f.cleaned_data["tag"].split()))
			instance.save()
			manage_requests()
		else:
			#content["form_errors"] = f.errors
			content["crawl_request_form"] = f
			return render(request, "fb_crawler/new_request.html", content)
		return HttpResponseRedirect(reverse("crawler_all"))
	
	# GET
	content["crawl_request_form"] = CrawlRequestForm()
	return render(request, "fb_crawler/new_request.html", content)

def get_file(request, filetype, request_id):
	crawler_object = get_object_or_404(CrawlRequest, pk=request_id)
	if crawler_object.status == "COM": #completed
		#filepath = os.path.join(
		#		MEDIA_ROOT,
		#		"%s.%s" % (crawler_object.filename, filetype))
		#return serve(request, filepath)
		return HttpResponseRedirect("/media/crawler_results/%s.%s" % (crawler_object.filename, filetype))
	return HttpResponseRedirect(reverse("crawler_all"))
