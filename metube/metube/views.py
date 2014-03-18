from django.shortcuts import render, HttpResponseRedirect
import logging

def home(request):
	content = {}
	return render(request, "index.html", content)
