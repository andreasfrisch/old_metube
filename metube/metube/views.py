from django.shortcuts import render
import logging

def home(request):
	content = {}
	return render(request, "index.html", content)
