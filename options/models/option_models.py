import time 
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from black_scholes_pricing import BlackScholes
from binomial_pricing import BinomialTree

"""
4/26

First priority
- Need to make r, sigma, q, S0 attributes of the Strategy class so that they are same for all options 
	- Either make them class attributes in the init - probably the better method
	- or adjust add_leg method so that only the first leg takes all inputs and the rest fetch values
- "Remove Leg" function
- Optimize attribute: if optimize = "speed", run fewer increments. if optimize = "detail", run more incrementss
- CONVERT method to convert strategy from one price model to another
- Create user input and limits for # steps, exercise type for Binomial model 

- Fix Binomial theta
- Work on scale for graphing - needs to take into account price model and the number of options in the strategy 



- Set up Controller

Second
- Improve speed of Binomial method if possible and optimize scale 
- Integrate basic controller 
- Make Web app

Luxury Goals / New Features
- Create Default Strategy Templates 
- Eliminate tracking error in BS models if possible
- Implied Volatility Calculator
- Exponentially Weighted Historical volatility (vs. Equally weighted h.v.)

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
	def __init__(self, model):
		self.legs = []
		self.model = model

	def data(self, option, S0, T): 
		"""
		Gets price and Greek values for an option. 
		"""
		return self.model(option, S0, T).data()

	def price(self, option, new_underlying_price, new_T): 
		return self.model(option, new_underlying_price, new_T).price() 

	def add_leg(self, position, kind, S0, K, T, q, r, sigma):
		"""
		Adds options to the strategy.
		"""
		def compare(item): 
			return item["exp"]
		new_leg = Option(position, kind, S0, K, T, q, r, sigma)
		data = self.data(new_leg, S0, T)
		time_exp = T
		self.legs.append({"option":new_leg, "data":data, "exp":time_exp})
		self.legs = sorted(self.legs, key=compare)

	def strategy_value(self, underlying_price): 
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
				profit = each["option"].option_profit(underlying_price, original_price)
				total_value += profit
				total_profit += profit
			else: 
				position = each["option"].position 
				if position == "long":
					new_T = each["exp"]-first_exp
					new_price = self.price(each["option"], underlying_price, new_T)
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

	def define_range(self, underlying_price): 
		"""
		Creates the index (x-axis) values for the strategy.
		The scale of the axis depends on the value of the underlying.
		"""
		start = underlying_price*1e-2
		end = underlying_price*2
		def scale(): 
			if underlying_price<20:
				return .01
			elif underlying_price<100: 
				return .05
			elif underlying_price<500: 
				return .25
			elif underlying_price<1000:
				return .50
			elif underlying_price<5000:
				return 2.50
			else:
				return False 
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
	new_strategy = Strategy(BinomialTree)
	new_strategy.add_leg("long", "call", 100, 100, 2, 0, .005, .25)
	new_strategy.add_leg("short", "call", 100, 100, 1, 0, .005, .25)
	price_range = new_strategy.define_range(100)
	df = new_strategy.dataframe_setup(price_range)
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








