import time 
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import uuid
from black_scholes_pricing import BlackScholes
from binomial_pricing import BinomialTree

"""
First priority
- CONVERT method to convert strategy from one price model to another
- Create user input and limits for # steps, exercise type for Binomial model 

- Fix Binomial theta
- Work on scale for graphing - needs to take into account price model and the number of options in the strategy 

- Set up Controller

Second
- Improve speed of Binomial method if possible and optimize scale 
- Integrate basic controller 

Luxury Goals / New Features
- Create Default Strategy Templates 
- Eliminate tracking error in BS models if possible
- Implied Volatility Calculator
- Exponentially Weighted Historical volatility (vs. Equally weighted h.v.)

"""

"""
Speed Optimization and Increments: 
- "Speed" vs "Detail" setting 
- Number of Expiration Dates: if no recalculations have to be made, speed is almost 100 times faster 
- Pricing Model: Black-Scholes is approx. 9x faster than Binomial Tree 
- Number of Options in the strategy 
- Keep track of number of expiration dates in the strategy in a list to prioritize speed? 
- # of steps in Binomial Tree method - 10 steps is 5x faster than 25 steps

Goal: rank all the different combinations of factors and come up with an algorithm that sets
the scale based on all the different inputs. Max latency for any calculation should be 1 second. 

"""

class Option: 
	"""
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

class Strategy: 
	"""
	Dynamic container for a set of option legs with the same underlying.
	Model argument for the class is the name of the class used for pricing the options 
	within the strategy - e.g. BlackScholes.

	Underlying price, risk free rate, dividend rate, and volatility must be identical 
	for all options in the strategy. 
	"""
	def __init__(self, model, S0, q, r, sigma):
		self.legs = []
		self.model = model
		self.S0 = S0
		self.q = q
		self.r = r
		self.sigma = sigma

	def data(self, option): 
		"""
		Gets price and Greek values for an option. 
		"""
		return self.model(option, self.S0, option.T).data()

	def price(self, option, new_underlying_price, new_T):
		"""
		For recalculating price of options in strategies with multiple expirations.
		"""
		return self.model(option, new_underlying_price, new_T).price() 

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
		time_exp = T
		self.legs.append({"option":new_leg, "data":data, "exp":time_exp, "id":str(uuid.uuid4())})
		self.legs = sorted(self.legs, key=compare)
		# Need to remove add functionality in web app if 6 legs present

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
			return total_cost, "net debit"
		elif total_cost<0: 
			return abs(total_cost), "net credit"

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
			print(each["id"])
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
		from 1/100 to 2x the underlying value.
		The scale of the axis depends on the value of the underlying.
		"""
		start = self.S0*1e-2
		end = self.S0*2
		def scale(): 
			if self.S0<20:
				return .01
			elif self.S0<100: 
				return .05
			elif self.S0<500: 
				return .25
			elif self.S0<1000:
				return .50
			elif self.S0<5000:
				return 2.50
			else:
				return (self.S0/400)
		scale = scale()
		return np.arange(start,end,scale)

	def dataframe_setup(self, price_range):
		"""
		Maps the value of the strategy at each price interval.
		Takes as an argument the range produced by define_range.
		"""
		df = pd.DataFrame(index=price_range) 
		df['strategy_value']=None
		df.strategy_value = df.index.map(lambda x: self.strategy_value(x)["profit"])
		return df

	# def plot_profit(self, df): 
	# 	"""
	# 	Takes as an argument the dataframe created by dataframe_setup and creates
	# 	a graph using matplotlib. 
	# 	"""
	# 	df.plot()
	# 	plt.show()

	def convert(self, model): 
		pass
		# Convert entire strategy to other price model

if __name__ == "__main__":
	time1 = time.time()
	new_strategy = Strategy(BlackScholes, 100, 0, .005, .25)
	# Calendar spread with calls
	new_strategy.add_leg("long", "call", 100, 2)
	new_strategy.add_leg("short", "call", 100, 1)
	# Double Diagonal
	# new_strategy.add_leg("short", "put", 90, 1)
	# new_strategy.add_leg("short", "call", 110, 1)
	# new_strategy.add_leg("long", "put", 70, 1.5)
	# new_strategy.add_leg("long", "call", 130, 1.5)
	df = new_strategy.dataframe_setup(new_strategy.define_range())
	elapsed = time.time() - time1
	print(elapsed)
	print(df)
	# new_strategy.plot_profit(df)

	#df.loc()[100]


# class LongCall(Strategy): 
# 	def __init__(self): 
# 		super().__init__(BlackScholes)
# 		self.add_leg("long", "call", 100, 110, 1, 0, .005, .25)

	# a = LongCall()
	# price_range = a.define_range(100)
	# df = a.dataframe_setup(price_range)
	# print(df)
	# a.plot_profit(df)







