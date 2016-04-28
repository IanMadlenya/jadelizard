from option_models import Option, Strategy
from pricing_utils import InputCalc


class Controller: 
	def __init__(self): 
		self.price_model = None
		self.strategy = []

	def create_strategy(self): 
		def choose_model():
			model = input("Choose a pricing model: Black-Scholes [1] Binomial Tree [2]")
			if model == '1':
				self.price_model = BlackScholes 
			elif model == '2':
				self.price_model = BinomialTree 
			else: 
				choose_model()
		choose_model()
		new_strategy = Strategy(self.price_model)
		self.strategy.append(new_strategy)
		print("Options strategy created.")

	def strategy_menu(self): 
		pass


	# Cost of Strategy Function
	# 