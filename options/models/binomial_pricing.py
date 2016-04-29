from numpy import exp
import numbers
from .basepricemodel import BasePriceModel

# Need to fix greeks and make sure they are at least ballpark Tching Binomial tree values on BlackScholes calc
# or values of a dedicated CRR tree calc

"""
Lattice-Based Binomial Pricing Model for American or European Options
Describes the price of the underlying over a period of time

For a European option, there is no option of early exercise, and the binomial value applies at all nodes
For an American option, since the option may either be held or exercised prior to expiry, 
the value at each node is max(Binomial Value, Exercise Value)

"""

class BinomialTree(BasePriceModel):
	def __init__(self, option, S0, T, exer_type=None, steps=None):
		super().__init__(option, S0, T)
		self.exer_type = exer_type or 'european'
		self.steps = steps or 25

	def copy(self):
		return type(self)(self.option.copy(), self.S0, self.T, self.exer_type, self.steps)

	def run(self, **kwargs):
		return self.binomial_tree(**kwargs)

	def binomial_tree(self, sens_degree=2, greeks=True):
		num_steps = self.steps
		val_cache = {}

		dt = float(self.T) / num_steps
		up_fact = exp(self.option.sigma * (dt ** 0.5))
		down_fact = 1.0 / up_fact
		cont_yield = 0 if callable(self.option.q) else self.option.q
		prob_up = (exp((self.option.r - cont_yield) * dt) - down_fact) / (up_fact - down_fact)

		def divs_pv(n):
			if not hasattr(self.option.q, '__call__'): return 0
			pv_divs = 0
			for step_num in range(n, num_steps):
				div_t1, div_t2 = dt * step_num, dt * (step_num + 1)
				div = self.option.q(div_t1, div_t2)
				if is_number(div):
					mid_div_t = 0.5 * (div_t1 + div_t2)
					pv_divs += exp(-self.option.r * mid_div_t) * div
			return pv_divs

		bin_S0 = self.S0 - divs_pv(0)

		def spot_price(n, num_ups, num_downs):
			return (bin_S0 + divs_pv(n)) * (up_fact ** (num_ups - num_downs))

		def node_value(n, num_ups, num_downs):
			value_cache_key = (n, num_ups, num_downs)
			if value_cache_key not in val_cache:
				spot = spot_price(n, num_ups, num_downs)
				if self.option.kind == 'call':
					exer_profit = max(0, spot - self.option.K)
				elif self.option.kind == 'put':
					exer_profit = max(0, self.option.K - spot)

				if n >= num_steps:
					val = exer_profit
				else:
					fv = prob_up * node_value(n + 1, num_ups + 1, num_downs) + \
						(1 - prob_up) * node_value(n + 1, num_ups, num_downs + 1)
					pv = exp(-self.option.r * dt) * fv
					if self.exer_type == 'american':
						val = max(pv, exer_profit)
					elif self.exer_type == 'european':
						val = pv

				val_cache[value_cache_key] = val
			return val_cache[value_cache_key]

		val = node_value(0, 0, 0)
		delta, theta, rho, vega, gamma = None, None, None, None, None
		if greeks and sens_degree >= 1:
			delta = (node_value(1, 1, 0) - node_value(1, 0, 1)) / (bin_S0 * up_fact - bin_S0 * down_fact)
			theta = (node_value(2, 1, 1) - val) / (2 * dt)

			rho = 1e-2*self.sensitivity('r', 0.0001, sens_degree=sens_degree - 1)
			vega = 1e-2*self.sensitivity('sigma', 0.001, sens_degree=sens_degree - 1)

			delta_up = (node_value(2, 2, 0) - node_value(2, 1, 1)) / (bin_S0 * up_fact - bin_S0 * down_fact)
			delta_down = (node_value(2, 1, 1) - node_value(2, 0, 2)) / (bin_S0 * up_fact - bin_S0 * down_fact)
			gamma = (delta_up - delta_down) / ((bin_S0 * up_fact * up_fact - bin_S0 * down_fact * down_fact) / 2)

		return {
			"price": val,
			"delta": delta,
			"theta": theta,
			"rho": rho,
			"vega": vega,
			"gamma": gamma,
		}

	def sensitivity(self, opt_param, opt_param_bump, **model_kwargs):
		up_model = self.copy()
		setattr(up_model.option, opt_param, getattr(up_model.option, opt_param) + opt_param_bump)
		down_model = self.copy()
		setattr(down_model.option, opt_param, getattr(down_model.option, opt_param) - opt_param_bump)
		up_measure = up_model.run(**model_kwargs)['price']
		down_measure = down_model.run(**model_kwargs)['price']
		return (up_measure - down_measure) / (2 * opt_param_bump)

	def data(self, **kwargs):
		return self.run(**kwargs)

	def price(self, **kwargs):
		kwargs['greeks'] = False
		return self.run(**kwargs)["price"]

def is_number(x):
	return (x is not None) and \
		   (isinstance(x, int) or isinstance(x, float) or isinstance(x, numbers.Integral))


