from django.shortcuts import render, HttpResponseRedirect
import logging

def home(request):
	return HttpResponseRedirect("/facebook_crawler");
