import pandas
from pandas import np
from pandas_datareader import data
import datetime
from dateutil import parser

class Utils:

	@staticmethod
	def trailing_volatility(ticker, days):
		"""
		Returns equally-weighted historical volatility for a stock during the last X trading days
		(annualized std deviation of daily log returns) using market close prices.
		Google API - data available from Jan 4, 2010 to present and is adjusted for stock splits.
		"""
		try:
			quotes = data.DataReader(ticker, 'google')['Close'][-days:]
		except Exception:
			return False 
		logreturns = np.log(quotes / quotes.shift(1))
		return round(np.sqrt(252*logreturns.var()), 5)

	"""
	Get risk free rate of return - gets monthly and daily 90 day T Bill rates from St. Louis Fed
	"""
	@staticmethod
	def get_r(): 
		try: 
			monthly = float(str(data.get_data_fred("GS3M").tail(1).values[0][0])[:5])/100
			daily = float(str(data.get_data_fred("DGS3MO").tail(1).values[0][0])[:5])/100
		except Exception:
			return False
		return {
		"monthly":round(monthly,4),
		"daily":round(daily,4), 
		}









