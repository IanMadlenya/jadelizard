from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import (
	Strategy, Option, BlackScholes, BinomialTree, Utils, Templates
)
from options.forms import StrategyForm, LegsForm, StockForm, PriceModelForm, VolForm, RangeForm

class Index(View): 
	template_name = "options/base.html"
	def get(self, request): 
		request.session["current_strategy"]=None
		request.session["current_model"] = BlackScholes.__name__
		request.session["graph_range"] = {"start":None,"end":None}
		return render(request, self.template_name)

class NewStrategy(View): 
	"""
	Save constants for the underlying instrument 
	"""
	def post(self, request): 
		form = StrategyForm(request.POST)
		if form.is_valid():
			form.clean_data()
			S0 = form.cleaned_data.get("S0")
			q = form.cleaned_data.get("q")
			r = form.cleaned_data.get("r")
			sigma = form.cleaned_data.get("sigma")
			request.session["current_strategy"] = Strategy(request.session["current_model"], S0, q, r, sigma).to_json()
			request.session["current_range"] = {"start":None,"end":None}
			return JsonResponse({"status":"success"})
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

class UpdateStrategy(View): 
	def post(self, request): 
		form = StrategyForm(request.POST)
		if form.is_valid(): 
			form.clean_data()
			strategy = Strategy.from_json(request.session["current_strategy"])
			S0 = form.cleaned_data.get("S0")
			q = form.cleaned_data.get("q")
			r = form.cleaned_data.get("r")
			sigma = form.cleaned_data.get("sigma")
			strategy.edit_strategy(S0, sigma, q, r)
			request.session["current_strategy"] = strategy.to_json()
			return JsonResponse({"status":"Strategy Values Updated"})
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

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
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

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
		models = {"BlackScholes":"Black-Scholes", "BinomialTree": "Binomial Tree"}
		model = models.get(request.session['current_model'])
		data = {"S0":round(strategy.S0, 2), "sigma":round(strategy.sigma, 5), "q":round(strategy.q, 5), "r":round(strategy.r, 5), "model":model}
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

class SetStock(View): 
	"""
	Set qty shares long/short
	"""
	def post(self, request): 
		form = StockForm(request.POST)
		if form.is_valid(): 
			strategy = Strategy.from_json(request.session["current_strategy"])
			longqty, shortqty = form.cleaned_data.get('longqty'), form.cleaned_data.get('shortqty')
			strategy.set_stock(longqty, shortqty)
			request.session["current_strategy"] = strategy.to_json()
			return JsonResponse({"status":"Shares Updated", "longqty":longqty, "shortqty":shortqty})
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
		start, end = request.session["graph_range"]["start"], request.session["graph_range"]["end"]
		json_data = strategy.graph_data(range_start=start, range_end=end)
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
			request.session["current_range"] = {"start":None,"end":None}
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
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

class GetR(View): 
	"""
	Fetch risk-free rate of return (90-Day Treasury)
	"""
	def get(self, request): 
		r = Utils.get_r()
		if not r:
			return JsonResponse({"status":"Error Retrieving Data"}, status=503)
		return JsonResponse(r) 

class StrategyTemplate(View): 
	"""
	Load a preset Strategy Template
	"""
	def post(self, request): 
		template = Templates.get(request.POST.get('id'))
		model = request.session["current_model"]
		request.session["current_strategy"]=template(model).to_json()
		request.session["graph_range"] = {"start":None,"end":None}
		return JsonResponse({"status":"Template Loaded"})

class GraphRange(View):
	"""
	Set a manual range for graphing
	"""
	def post(self, request): 
		form = RangeForm(request.POST)
		if form.is_valid(): 
			form.clean_data()
			if form.errors:
				invalid_fields = {"fields":form.errors.as_json()}
				return JsonResponse(invalid_fields)
			start = form.cleaned_data.get('range_start')
			request.session["graph_range"]["start"]=form.cleaned_data.get('range_start')
			request.session["graph_range"]["end"]=form.cleaned_data.get('range_end')
			request.session.modified = True
			return JsonResponse({"status":"Range Updated"})
		invalid_fields = {"fields":form.errors.as_json()}
		return JsonResponse(invalid_fields)

class ResetRange(View): 
	"""
	Revert to auto window setting
	"""
	def post(self, request): 
		request.session["graph_range"] = {"start":None,"end":None}
		return JsonResponse({"status":"Window Reset"})






				