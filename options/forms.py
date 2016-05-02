from django import forms 

class NewStrategyForm(forms.Form):
	S0 = forms.DecimalField(label='Price of Underlying', min_value=1, max_value=1000, decimal_places=2)
	sigma = forms.DecimalField(label='Volatility of Underlying', min_value=0, max_value=0.9999, decimal_places=4)
	q = forms.DecimalField(label='Continuously Compounded Dividend Yield', min_value=0, max_value=0.9999, decimal_places=4)
	r = forms.DecimalField(label='Risk-Free Rate', min_value=0, max_value=0.9999, decimal_places=4)

class LegsForm(forms.Form): 
	pass
