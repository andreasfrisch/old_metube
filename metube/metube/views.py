from django.shortcuts import render

def home(request):
	content = {}
	return render(request, "index.html", content)
