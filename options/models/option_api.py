from pandas_datareader import data

def all_option_data(ticker): 
	try:
		all_data = data.Options(ticker, 'yahoo').get_all_data()
	except Exception: 
		print("Error getting data for symbol '{}'.".format(ticker))
		return False
	return all_data


