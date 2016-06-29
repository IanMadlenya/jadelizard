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
		self.shares = {"longqty": 0, "shortqty": 0}
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

	def edit_strategy(self, S0, sigma, q, r): 
		"""
		Change underlying values for the strategy and re-price legs with the new values. 
		"""
		self.S0 = S0
		self.sigma = sigma
		self.q = q
		self.r = r
		for each in self.legs: 
			option = each["option"]
			edited_leg = Option(option.position, option.kind, self.S0, option.K, option.T, self.q, self.r, self.sigma)
			data = self.data(edited_leg)
			each["option"] = edited_leg
			each["data"] = data

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

	def set_stock(self, longqty, shortqty):
		"""
		Add or remove shares of stock from the strategy 
		"""
		self.shares['longqty'], self.shares['shortqty'] = longqty, shortqty 

	def strategy_value(self, new_underlying_price): 
		"""
		The return value - profit - is the value used for graphing. It includes profit or loss from options
		at the first expiration, plus the unrealized gain/loss of the adjusted value of outstanding long options
		minus their initial cost, plus credit received from outstanding short options, plus unrealized gain/loss
		from shares of stock (long and short). 

		It is not possible to assess the value of a strategy at multiple points in time, meaning that, in a 
		strategy with multiple expiration dates, valuation for the longer-term options can be problematic. 
		These calculations do not take into account the profit/loss from those longer-term legs at expiration. 

		In addition: the assumption must be made that interest rates and volatility of the underlying at expiration 
		of the earliest options are the same as when the strategy is initiated. This will not necessarily be the case.
		"""
		total_profit = 0
		first_exp = self.legs[0]["exp"]
		for each in self.legs: 
			original_price = each["data"]["price"]
			if each["exp"] == first_exp: 
				total_profit += each["option"].option_profit(new_underlying_price, original_price)
			else: 
				position = each["option"].position 
				if position == "long":
					new_T = each["exp"]-first_exp
					new_price = self.price(each["option"], new_underlying_price, new_T)
					total_profit += new_price - original_price
				elif position == "short": 
					total_profit += original_price
		# Add P/L for Stock Shares
		long_pl = self.shares["longqty"]*(new_underlying_price - self.S0)
		short_pl = self.shares["shortqty"]*(self.S0 - new_underlying_price)
		total_profit += (long_pl + short_pl)

		return total_profit

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
		total_cost += self.shares['longqty']*self.S0
		total_cost -= self.shares['shortqty']*self.S0
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

	def define_range(self, range_start=None, range_end=None): 
		"""
		Creates the index and price range (x-axis) for the strategy. 
		Default is to calculate P/L from 25 percent to 200 percent underlying value. 
		The user can also enter a desired range for graphing.

		The graph_range variable determines the scale for the graph. The goal is to generate
		no fewer than 100 and no more than 400 data points for graphing, with 200 being ideal. 
		D3/C3 generally don't work as well once datasets exceed that size. 
		"""
		if range_end: 
			start,end = range_start,range_end
			graph_range = (range_end-range_start)/1.75
		else: 
			start, end = (int(self.S0*0.25)+1), (int(self.S0*2)+1)
			graph_range = self.S0
		def scale(): 
			if graph_range<2:
				return .02
			elif graph_range<5: 
				return .05
			elif graph_range<10: 
				return .10
			elif graph_range<20: 
				return .20
			elif graph_range<50: 
				return .25
			elif graph_range<100: 
				return .50
			elif graph_range<200: 
				return 1
			elif graph_range<500: 
				return 2.50
			elif graph_range<=1000: 
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
		df['strategy_profit'] = df.price_range.map(lambda x: self.strategy_value(x))
		return df

	def graph_data(self, range_start=None, range_end=None): 
		"""
		Returns copy of dataframe for graphing in C3
		"""
		cols = self.define_range(range_start, range_end)
		df = self.dataframe_setup(cols[0], cols[1])
		return df.to_json(orient='records')

	def legs_data(self): 
		"""
		Returns legs-specific data for display, sorted by strike price
		"""
		def compare(item): 
			return (item["T"], item["K"], item["position"], item["kind"])
		legs = []
		for each in self.legs: 
			option = each["option"]
			legs.append({"position":option.position.upper(), "kind":option.kind.upper(), "K":option.K, "T":option.T, "id":each["id"]})
		legs = sorted(legs, key=compare)
		return legs

	def leg_by_id(self, id_): 
		"""
		Returns leg data by UUID
		"""
		for each in self.legs: 
			if each["id"]==id_:
				return {
					"position":each["option"].position,
					"kind":each["option"].kind,
					"K":each["option"].K,
					"T":each["option"].T, 
					"id":each["id"]
				} 

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
		"legs": [{"data":leg["data"], "id": leg["id"], "exp": leg["exp"], "option" :leg["option"].to_json()} for leg in self.legs], 
		"shares": self.shares
		}

	@classmethod
	def from_json(cls, data): 
		strategy = cls(data["model"], data["S0"], data["q"], data["r"], data["sigma"])
		strategy.exer_type = data["exer_type"]
		strategy.steps = data["steps"]
		legs = data["legs"]
		strategy.legs = [{"data":leg["data"], "id":leg["id"], "exp":leg["exp"], "option":Option.from_json(leg["option"])} for leg in legs]
		strategy.shares = data["shares"]
		return strategy

