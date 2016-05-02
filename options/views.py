from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import (
	Strategy, Option, BlackScholes, BinomialTree, InputCalc
)
from options.forms import NewStrategyForm, LegsForm

class Index(View): 
	template_name = "options/base.html"
	def get(self, request): 
		request.session["current_model"]=BlackScholes.__name__
		return render(request, self.template_name)

class NewStrategy(View): 
	def post(self, request): 
		form = NewStrategyForm(request.POST)
		if form.is_valid():
			S0 = form.data.get("S0")
			q = form.data.get("q")
			r = form.data.get("r")
			sigma = form.data.get("sigma")
			print(data)
			request.session["current_strategy"] = Strategy(request.session["current_model"], S0, q, r, sigma).to_json()
			return JsonResponse({"status":"success"})
		return JsonResponse({"status":"Invalid or Missing Input"})

class AddLeg(View): 
	def get(self, request): 
		pass

class DeleteLeg(View): 
	def get(self, request): 
		pass


class GraphData(View): 
	def get(self, request): 
		new_strategy = Strategy(BlackScholes, 100, .05, .005, .50)
		new_strategy.convert(BinomialTree)
		new_strategy.model_settings('european', 25)
		# new_strategy.add_leg("long", "call", 100, 2)
		# new_strategy.add_leg("short", "call", 100, 1)
		new_strategy.add_leg("short", "put", 75, 1)
		new_strategy.add_leg("short", "call", 110, 1)
		new_strategy.add_leg("long", "put", 70, 1.5)
		new_strategy.add_leg("long", "call", 130, 1.5)
		json_data = new_strategy.run_models()
		return JsonResponse(json_data,safe=False)

class ChooseModel(View): 
	def post(self, request): 
		model = request.session["current_model"]
		request.session["current_strategy"].convert()
		pass


				