import numpy as np
import scipy.stats as ss
from scipy import exp, log
from basepricemodel import BasePriceModel

"""

-Black Scholes Model for Pricing European Call and Put Options-
-Pricing of options that can only be exercised at the expiration date-
-Arguments: 
	S0 - Stock Price
	K - Strike Price
	r - continuously compounded risk-free rate of return (as decimal)
	sigma - volatility of the stock price per year (as decimal)
	T - time to expiration in trading years
	kind - call or put
	q - Continuously compounded dividend yield

- Greeks: 
	Delta - Rate of change of option price with respect to change in underlying asset price
	Theta - Sensitity of option price to passage of time (time decay)
	Vega - Rate of change of option price with respect to change in volatility (same for call/put)
	Rho - Rate of change of option price with respect to change in risk-free interest rate
	Gamma - Rate of change of delta with respect to change in underlying price (same for call/put)

"""

class BlackScholes(BasePriceModel): 
	def __init__(self, option, S0, T):
		super().__init__(option, S0, T) 
		self.d1 = self.d1()
		self.d2 = self.d2()

	def d1(self):
		return (np.log(self.S0/self.option.K) + (self.option.r - self.option.q + self.option.sigma**2 / 2) \
			* self.T)/(self.option.sigma * np.sqrt(self.T))
	
	def d2(self):
		return self.d1 - self.option.sigma*np.sqrt(self.T)

	def calculate_price(self):
		if self.option.kind=="call":
			return self.S0 * exp(-self.option.q * self.T) * ss.norm.cdf(self.d1) - \
			self.option.K * exp(-self.option.r * self.T) * ss.norm.cdf(self.d2)
		elif self.option.kind=="put":
		   return self.option.K * exp(-self.option.r * self.T) * ss.norm.cdf(-self.d2) - \
		   self.S0 * exp(-self.option.q * self.T) * ss.norm.cdf(-self.d1)

	def delta(self):
		N = ss.norm.cdf  
		if self.option.kind == "call":            
			return exp(-self.option.q * self.T) * N(self.d1)
		else:
			return exp(-self.option.q * self.T) * (N(self.d1)-1)

	def gamma(self): 
		return exp(-self.option.q * self.T) * (ss.norm.pdf(self.d1) / (self.S0 * self.option.sigma * np.sqrt(self.T)))

	def rho(self): 
		N = ss.norm.cdf
		if self.option.kind == "call": 
			return 1e-2 * self.option.K * self.T * exp(-self.option.r * self.T) * N(self.d2)
		elif self.option.kind == "put": 
			return -1e-2 * self.option.K * self.T * exp(-self.option.r * self.T) * N(-self.d2)

	def theta(self): 
		N = ss.norm.cdf
		r_exp = exp(-self.option.r * self.T)
		q_exp = exp(-self.option.q * self.T)
		if self.option.kind == "call": 
			result = -1 * q_exp * (self.S0 * ss.norm.pdf(self.d1) * self.option.sigma) / (2 * np.sqrt(self.T)) \
			- self.option.r * self.option.K * r_exp * N(self.d2) + self.option.q * self.S0 * q_exp * N(self.d1)
			return result/365
		elif self.option.kind == "put": 
			result = -1 * q_exp * (self.S0 * ss.norm.pdf(self.d1) * self.option.sigma) / (2 * np.sqrt(self.T)) \
			+ self.option.r * self.option.K * r_exp * N(-self.d2) - self.option.q * self.S0 * q_exp * N(-self.d1)
			return (1/365)*result

	def vega(self):
		return 1e-2 * self.S0 * exp(-self.option.q * self.T) * np.sqrt(self.T) * ss.norm.pdf(self.d1)

	def data(self): 
		return {
			"price":self.calculate_price(),
			"delta":self.delta(),
			"gamma":self.gamma(),
			"rho":self.rho(),
			"theta":self.theta(),
			"vega":self.vega()
		}

	def price(self): 
		# return {
		# 	"price":self.calculate_price()
		# }
		return self.calculate_price()





