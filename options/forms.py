from django import forms 

POSITION_CHOICES=[
("BUY", "Long"),
("SELL", "Short")
]

KIND_CHOICES=[
("c", "Call"), 
("p", "Put")
]

class NewStrategyForm(forms.Form):
	S0 = forms.DecimalField(min_value=1, max_value=1000, decimal_places=2)
	sigma = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)
	q = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)
	r = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)

class LegsForm(forms.Form): 
	position = forms.TypedChoiceField(choices=POSITION_CHOICES, empty_value="BUY")
	kind = forms.TypedChoiceField(choices=KIND_CHOICES, empty_value="c")
	K = forms.DecimalField(min_value=1, max_value=1000, decimal_places=2)
	T = forms.DecimalField(min_value=.00272, max_value=100, decimal_places=4)
