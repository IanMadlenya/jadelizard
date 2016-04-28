class BasePriceModel:
	def __init__(self, option, S0, T):
		self.option = option
		self.S0 = S0
		self.T = T

	def data(self): 
		"""
		Gets Option Price and Greeks at strategy initialization
		"""
		raise NotImplementedError()

	def price(self):
		"""
		Gets Option Price - intended to calculate adjusted price for 
		strategies with multiple expiration dates 
		"""
		raise NotImplementedError()