from django.shortcuts import render

def home(request):
	content = {}
	return render(request, "project_tracker/index.html", content)
