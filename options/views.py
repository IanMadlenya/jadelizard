from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

class Index(View): 
	template_name = "options/base.html"
	def get(self, request): 
		return render(request, self.template_name)

class NavBar(View): 
	def get(self, request): 
		pass