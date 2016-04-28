import pandas
from pandas import np
from pandas_datareader import data
import datetime
from dateutil import parser

class InputCalc:

	@staticmethod
	def trailing_volatility(ticker, days):
		"""
		Returns equally-weighted historical volatility for a stock during the last X trading days
		(annualized std deviation of daily log returns) using market close prices.
		Google API - data available from Jan 4, 2010 to present and is adjusted for stock splits.
		"""
		# if days<10: 
		# 	raise ValueError("Trailing period must be 10+ days.")
		try:
			quotes = data.DataReader(ticker, 'google')['Close'][-days:]
		except Exception:
			print("Error getting data for symbol '{}'.".format(ticker))
			return False 
		logreturns = np.log(quotes / quotes.shift(1))
		return np.sqrt(252*logreturns.var())

	"""
	Range Volatility - returns annualized daily volatility for a stock during the provided date range
	Format for date input: Y-m-d or Ymd 
	"""
	@staticmethod
	def range_volatility(ticker, start, end):
		try:
			quotes = data.DataReader(ticker, 'google')['Close'].loc[start:end]
		except Exception:
			print("Error getting data for symbol '{}'.".format(ticker))
			return False 
		logreturns = np.log(quotes / quotes.shift(1))
		return np.sqrt(252*logreturns.var())


	"""
	Get risk free rate of return - gets monthly and daily 90 day T Bill rates from St. Louis Fed
	"""
	@staticmethod
	def get_r(): 
		try: 
			monthly = float(str(data.get_data_fred("GS3M").tail(1).values[0][0])[:5])/100
			daily = float(str(data.get_data_fred("DGS3MO").tail(1).values[0][0])[:5])/100
		except Exception:
			print("Error getting FRED data")
			return False
		return {
		"monthly":monthly,
		"daily":daily, 
		}

	"""
	Converts difference between input date and present date to duration in years
	"""
	@staticmethod
	def date_to_years(date): 
		now = datetime.date.today()
		exp = parser.parse(date).date()
		years = (exp-now).days/365
		if years < 0: 
			return False
		return years









