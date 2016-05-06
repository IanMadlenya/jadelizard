import time 
import pandas as pd
import numpy as np
import uuid
from .black_scholes_pricing import BlackScholes
from .binomial_pricing import BinomialTree

class Option: 
	"""
	Option objects are the building blocks ("legs") for Options Strategies. 

	Position - "long" or "short"
	Kind - "call" or "put"
	S0 - underlying price of security
	K - Strike price
	T - time to expiration, in years
	q - compounded annual dividend yield
	r - risk-free rate of return 
	sigma - annualized volatility of underlying
	"""
	def __init__(self, position, kind, S0, K, T, q, r, sigma): 
		self.position = position
		self.kind = kind
		self.S0 = S0
		self.K = K
		self.T = T
		self.q = q
		self.r = r
		self.sigma = sigma

	def copy(self):
		return type(self)(self.position, self.kind, self.S0, self.K, self.T, self.q, self.r, self.sigma)

	def option_profit(self, current_underlying_price, option_price):
		"""
		calculates the value of an options contract (long/short, put/call) at expiration
		"""
		if self.kind == "call" and self.position == "long":
			if current_underlying_price <= self.K: 
				return (-option_price)
			elif current_underlying_price > self.K: 
				return (current_underlying_price - self.K) - option_price

		elif self.kind == "put" and self.position == "long":
			if current_underlying_price >= self.K: 
				return (-option_price)
			elif current_underlying_price < self.K: 
				return (self.K - current_underlying_price) - option_price 

		elif self.kind == "call" and self.position == "short": 
			if current_underlying_price <= self.K: 
				return option_price 
			elif current_underlying_price > self.K: 
				return option_price - (current_underlying_price - self.K)

		elif self.kind == "put" and self.position == "short": 
			if current_underlying_price >= self.K: 
				return option_price 
			elif current_underlying_price < self.K: 
				return option_price - (self.K - current_underlying_price)

	def to_json(self): 
		return {"position":self.position, 
				"kind":self.kind,
				"S0":self.S0,
				"K":self.K,
				"T":self.T,
				"q":self.q,
				"r":self.r,
				"sigma":self.sigma}

	@classmethod
	def from_json(cls, data):
		return cls(data["position"], data["kind"], data["S0"], data["K"], data["T"], data["q"], data["r"], data["sigma"])

class Strategy: 
	"""
	Dynamic container for a set of option legs with the same underlying.
	Model argument for the class is the name of the class used for pricing the options 
	within the strategy - e.g. BlackScholes.

	Underlying price, risk free rate, dividend rate, and volatility must be identical 
	for all options in the strategy. 
	"""

	pricing_models = {"BlackScholes":BlackScholes, "BinomialTree":BinomialTree}

	def __init__(self, model_name, S0, q, r, sigma):
		self.legs = []
		self.model = self.pricing_models.get(model_name)
		self.S0 = S0
		self.q = q
		self.r = r
		self.sigma = sigma
		self.exer_type = None
		self.steps = None

	def model_settings(self, model_name, exer_type, steps): 
		""" 
		Converts the strategy to the price model given by the argument. 
		"""
		self.model=self.pricing_models.get(model_name)
		self.exer_type=exer_type
		self.steps=steps
		for each in self.legs: 
			option = each["option"]
			each["data"] = self.data(option)

	def data(self, option): 
		"""
		Gets price and Greek values for an option. 
		"""
		return self.model(option, self.S0, option.T, exer_type=self.exer_type, steps=self.steps).data()

	def price(self, option, new_underlying_price, new_T):
		"""
		For recalculating price of options in strategies with multiple expirations.
		"""
		return self.model(option, new_underlying_price, new_T, exer_type=self.exer_type, steps=self.steps).price() 

	def add_leg(self, position, kind, K, T):
		"""
		Adds options to the strategy. 
		Each leg is a dictionary with the original Option object, the original price and greek values
		calculated with the set pricing model, its expiration (which is used to sort the list of legs), 
		and a UUID. 
		"""
		def compare(item): 
			return item["exp"]
		new_leg = Option(position, kind, self.S0, K, T, self.q, self.r, self.sigma)
		data = self.data(new_leg)
		self.legs.append({"option":new_leg, "data":data, "exp":T, "id":str(uuid.uuid4())})
		self.legs = sorted(self.legs, key=compare)

	def remove_leg(self, _id):
		for each in self.legs: 
			if each["id"] == _id: 
				self.legs.remove(each)
				return "Leg removed"

	def strategy_value(self, new_underlying_price): 
		"""
		This function returns three values: 

		1. Value - total value of the options strategy – profit or loss from options at first expiration, 
		plus the adjusted price of any long outstanding options at first expiration, plus the net credit
		received from short options outstanding at first expiration.

		2. Profit - This is the value used for graphing. Profit or loss from options at first expiration, 
		plus the unrealized gain/loss of the adjusted value of outstanding long options minus their initial 
		cost, plus net credit received from outstanding short options. 

		3. Remaining options - The adjusted value of outstanding long options. 

		If multiple expiration dates are present, the value method will calculate the value of the strategy 
		at the first expiration present - profit from options at the first expiration plus adjusted (at new T, S0)
		value of outstanding long options and credit received from outstanding short options. 

		In addition: the assumption is made that interest rates and 
		volatility of the underlying at expiration of the earliest options are the same as when the
		strategy is initiated. This will not necessarily be the case.
		"""
		total_value = total_profit = remaining_options = 0
		first_exp = self.legs[0]["exp"]
		for each in self.legs: 
			original_price = each["data"]["price"]
			if each["exp"] == first_exp: 
				profit = each["option"].option_profit(new_underlying_price, original_price)
				total_value += profit
				total_profit += profit
			else: 
				position = each["option"].position 
				if position == "long":
					new_T = each["exp"]-first_exp
					new_price = self.price(each["option"], new_underlying_price, new_T)
					total_value += new_price
					remaining_options += new_price
					total_profit += new_price - original_price
				elif position == "short": 
					total_value += original_price
					total_profit += original_price
		return {
			"value":total_value, 
			"profit":total_profit, 
			"rem_long_options":remaining_options
		}

	def strategy_cost(self): 
		"""
		Calculates the cost of creating the strategy - premiums paid minus premiums received.
		"""
		total_cost=0
		for each in self.legs: 
			cost = each["data"]["price"]
			position = each["option"].position
			if position == "long":
				total_cost += cost
			elif position == "short":
				total_cost -= cost 
		if total_cost>0: 
			return {"cost":total_cost, "type": "net debit"}
		elif total_cost<0: 
			return {"cost":abs(total_cost), "type": "net credit"}

	def strategy_greeks(self):
		"""
		Computes the Greek values at the initiation of the strategy 
		(Greek values of short options are the inverse of those for long options)
		"""
		delta=0
		gamma=0
		rho=0
		theta=0
		vega=0
		for each in self.legs: 
			position = each["option"].position
			if position == "long":
				delta+=each["data"]["delta"]
				gamma+=each["data"]["gamma"]
				rho+=each["data"]["rho"]
				theta+=each["data"]["theta"]
				vega+=each["data"]["vega"]
			elif position == "short":
				delta-=each["data"]["delta"]
				gamma-=each["data"]["gamma"]
				rho-=each["data"]["rho"]
				theta-=each["data"]["theta"]
				vega-=each["data"]["vega"]
		return {
		"delta":delta,
		"gamma":gamma,
		"rho":rho,
		"theta":theta,
		"vega":vega
		}

	def define_range(self): 
		"""
		Creates the index (x-axis) values for the strategy - 
		from 0 to 2x the underlying value.
		The scale of the axis depends on the value of the underlying.
		"""
		start = int(self.S0*0.25)+1
		end = int(self.S0*2)+1
		def scale(): 
			if self.S0<5: 
				return .05
			elif self.S0<10: 
				return .10
			elif self.S0<20: 
				return .20
			elif self.S0<50: 
				return .25
			elif self.S0<100: 
				return .50
			elif self.S0<200: 
				return 1
			elif self.S0<500: 
				return 2.50
			elif self.S0<=1000: 
				return 5
		scale = scale()
		price_range = np.arange(start,end,scale)
		index = np.arange(0,len(price_range), 1)
		return index, price_range

	def dataframe_setup(self, index, price_range):
		"""
		Maps the value of the strategy at each price interval.
		Takes as an argument the range produced by define_range.
		"""
		df = pd.DataFrame(index=index) 
		df['price_range']=price_range
		df['strategy_profit'] = df.price_range.map(lambda x: self.strategy_value(x)["profit"])
		return df

	def graph_data(self): 
		"""
		Returns copy of dataframe for graphing in C3
		"""
		cols = self.define_range()
		df = self.dataframe_setup(cols[0], cols[1])
		return df.to_json(orient='records')

	def legs_data(self): 
		"""
		Returns legs-specific data for display 
		"""
		legs = []
		for each in self.legs: 
			option = each["option"]
			legs.append({"position":option.position.upper(), "kind":option.kind.upper(), "K":option.K, "T":option.T, "id":each["id"]})
		return legs

	def valid_graph(self): 
		"""
		If no legs are present, graphing is disabled
		"""
		if len(self.legs)==0: 
			return False

	def valid_legs(self): 
		"""
		Maximum of 6 legs for graphing
		"""
		if len(self.legs)==6:
			return False

	def to_json(self): 
		return {
		"model":self.model.__name__,
		"S0":self.S0,
		"q":self.q,
		"r":self.r,
		"sigma":self.sigma,
		"exer_type":self.exer_type,
		"steps":self.steps,
		"legs": [{"data":leg["data"], "id": leg["id"], "exp": leg["exp"], "option" :leg["option"].to_json()} for leg in self.legs]
		}

	@classmethod
	def from_json(cls, data): 
		strategy = cls(data["model"], data["S0"], data["q"], data["r"], data["sigma"])
		strategy.exer_type = data["exer_type"]
		strategy.steps = data["steps"]
		legs = data["legs"]
		strategy.legs = [{"data":leg["data"], "id":leg["id"], "exp":leg["exp"], "option":Option.from_json(leg["option"])} for leg in legs]
		return strategy


# class LongCall(Strategy): 
# 	def __init__(self): 
# 		super().__init__(BlackScholes)
# 		self.add_leg("long", "call", 100, 110, 1, 0, .005, .25)







