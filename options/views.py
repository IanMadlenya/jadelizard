from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .models import (
	Strategy, Option, BlackScholes, BinomialTree, InputCalc
)

class Index(View): 
	template_name = "options/base.html"
	def get(self, request): 
		return render(request, self.template_name)

class GraphData(View): 
	def get(self, request): 
		new_strategy = Strategy(BlackScholes, 100, 0, .005, .25)
		# new_strategy.add_leg("long", "call", 100, 2)
		# new_strategy.add_leg("short", "call", 100, 1)
		new_strategy.add_leg("short", "put", 75, 1)
		new_strategy.add_leg("short", "call", 110, 1)
		new_strategy.add_leg("long", "put", 70, 1.5)
		new_strategy.add_leg("long", "call", 130, 1.5)
		cols = new_strategy.define_range()
		df = new_strategy.dataframe_setup(cols[0], cols[1])
		df_json = df.to_json(orient='records')
		return JsonResponse(df_json,safe=False)

				