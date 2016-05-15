from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import (
	Strategy, Option, BlackScholes, BinomialTree, Utils
)
from options.forms import NewStrategyForm, LegsForm, PriceModelForm, VolForm

class Index(View): 
	template_name = "options/base.html"
	def get(self, request): 
		request.session["current_strategy"]=None
		request.session["current_model"] = BlackScholes.__name__
		return render(request, self.template_name)

class NewStrategy(View): 
	"""
	Save constants for the underlying instrument 
	"""
	def post(self, request): 
		form = NewStrategyForm(request.POST)
		if form.is_valid():
			S0 = form.cleaned_data.get("S0")
			q = form.cleaned_data.get("q")
			r = form.cleaned_data.get("r")
			sigma = form.cleaned_data.get("sigma")
			request.session["current_strategy"] = Strategy(request.session["current_model"], S0, q, r, sigma).to_json()
			return JsonResponse({"status":"success"})
		return JsonResponse({"status":"Invalid or Missing Input"}, status=412)

class AddLeg(View): 
	"""
	Add leg to strategy (up to 6)
	"""
	def post(self, request):
		form = LegsForm(request.POST)
		strategy = Strategy.from_json(request.session["current_strategy"])
		if strategy.valid_legs()==False: 
			return JsonResponse({"status":"Max Strategy Size Reached"}, status=422) 
		if form.is_valid(): 
			position = form.cleaned_data.get("position")
			kind = form.cleaned_data.get("kind")
			K = form.cleaned_data.get("K")
			T = form.cleaned_data.get("T")
			strategy.add_leg(position, kind, K, T)
			request.session["current_strategy"] = strategy.to_json()
			return JsonResponse({"status":"success"})
		return JsonResponse({"status":"Invalid or Missing Input"})

class DisplayLegs(View): 
	"""
	Fetch all legs for display
	"""
	def get(self, request): 
		strategy = Strategy.from_json(request.session["current_strategy"])
		data = strategy.legs_data()
		return JsonResponse({'legs':data})

class StrategyInfo(View): 
	"""
	Fetch user entered values for the strategy for display
	"""
	def get(self, request): 
		strategy = Strategy.from_json(request.session["current_strategy"])
		data = {"S0":round(strategy.S0, 2), "sigma":round(strategy.sigma, 7), "q":round(strategy.q, 7), "r":round(strategy.r, 7)}
		return JsonResponse(data)

class DeleteLeg(View): 
	"""
	Delete individual leg selected by UUID
	"""
	def post(self, request): 
		strategy = Strategy.from_json(request.session["current_strategy"])
		id_ = request.POST.get('id')
		for each in strategy.legs: 
			if each["id"]==id_: 
				strategy.legs.remove(each)
		request.session["current_strategy"] = strategy.to_json()
		return JsonResponse({"status":"Leg Deleted"})

class GetLeg(View): 
	"""
	Get individual leg data by UUID
	"""
	def get(self, request): 
		strategy = Strategy.from_json(request.session["current_strategy"])
		id_ = request.GET.get('id')
		data = strategy.leg_by_id(id_)
		return JsonResponse(data)

class UpdateLeg(View): 
	"""
	Update values for a preexisting Leg
	"""
	def post(self, request): 
		form = LegsForm(request.POST)
		if form.is_valid(): 
			strategy = Strategy.from_json(request.session["current_strategy"])
			id_ = request.POST.get('id')
			position = form.cleaned_data.get('position')
			kind = form.cleaned_data.get('kind')
			K = form.cleaned_data.get('K')
			T = form.cleaned_data.get('T')
			for each in strategy.legs: 
				if each["id"]==id_: 
					strategy.remove_leg(id_)
					strategy.add_leg(position, kind, K, T)
			request.session["current_strategy"] = strategy.to_json()
			return JsonResponse({"status":"Leg Updated"})
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

class GraphData(View): 
	"""
	Get JSON (orient=records) with pricing index (x) and strategy P/L (y) for graphing
	"""
	def get(self, request): 
		if request.session["current_strategy"]==None: 
			return JsonResponse({"status":"No Strategy Present"}, status=412)
		strategy = Strategy.from_json(request.session["current_strategy"])
		if strategy.valid_graph()==False: 
			return JsonResponse({"status":"No Options in Strategy"}, status=422)
		S0 = strategy.S0
		json_data = strategy.graph_data()
		return JsonResponse({"data":json_data, "S0":S0})

class ClearData(View): 
	"""
	Clear the current strategy in the session
	"""
	def post(self, request): 
		if request.session["current_strategy"]==None: 
			return JsonResponse({"status":"No Strategy Present"})
		else: 
			request.session["current_strategy"] = None
			return JsonResponse({"status":"Strategy Cleared"})

class StrategyData(View):
	"""
	Get Strategy Setup Cost and Greek Values
	"""
	def get(self, request): 
		strategy = Strategy.from_json(request.session["current_strategy"])
		if len(strategy.legs)==0:
			return JsonResponse({"status":"No Options in Strategy"})
		greeks = strategy.strategy_greeks()
		cost = strategy.strategy_cost()
		data = {
		"delta":round(greeks["delta"], 5),
		"gamma":round(greeks["gamma"], 5),
		"rho":round(greeks["rho"], 5),
		"theta":round(greeks["theta"], 5),
		"vega":round(greeks["vega"], 5), 
		"cost":round(cost["cost"], 2),
		"type":cost["type"]
		}
		return JsonResponse(data)

class ChooseModel(View): 
	"""
	Set Model, Steps, Exercise Type, Reprice Options in Strategy
	"""
	def post(self, request): 
		form = PriceModelForm(request.POST)
		if form.is_valid(): 
			model = form.cleaned_data.get('model')
			exer_type = form.cleaned_data.get("exer_type")
			steps = form.cleaned_data.get("steps")
			request.session["current_model"] = model
			strategy = Strategy.from_json(request.session["current_strategy"])
			strategy.model_settings(model, exer_type, steps)
			request.session["current_strategy"] = strategy.to_json()
			return JsonResponse({"status":"Pricing Model Settings Updated"})
		return JsonResponse({"status":"Invalid or Missing Input"})

class TrailingVol(View): 
	"""
	Get volatility by ticker for given # of trailing days
	"""
	def get(self, request):
		form = VolForm(request.GET)
		if form.is_valid(): 
			ticker = form.data.get('ticker')
			days = int(form.data.get('days'))
			vol = Utils.trailing_volatility(ticker, days)
			if not vol: 
				return JsonResponse({"status":"Error Getting Volatility Data"}, status=503)
			return JsonResponse({"vol":vol})
		return JsonResponse({"status":"Invalid or Missing Input"})

class GetR(View): 
	"""
	Fetch risk-free rate of return (90-Day Treasury)
	"""
	def get(self, request): 
		r = Utils.get_r()
		if not r:
			return JsonResponse({"status":"Error Retrieving Data"}, status=503)
		return JsonResponse(r) 




				