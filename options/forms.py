from django import forms 

POSITION_CHOICES=[
("long", "long"),
("Short", "short")
]

KIND_CHOICES=[
("call", "call"), 
("put", "put")
]

# class NewStrategyForm(forms.Form):
# 	S0 = forms.DecimalField(min_value=1, max_value=1000, decimal_places=2)
# 	sigma = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)
# 	q = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)
# 	r = forms.DecimalField(min_value=0, max_value=0.9999, decimal_places=4)

# class LegsForm(forms.Form): 
# 	position = forms.TypedChoiceField(choices=POSITION_CHOICES)
# 	kind = forms.TypedChoiceField(choices=KIND_CHOICES)
# 	K = forms.DecimalField(min_value=1, max_value=1000, decimal_places=2)
# 	T = forms.DecimalField(min_value=.00272, max_value=100, decimal_places=4)

class NewStrategyForm(forms.Form):
	S0 = forms.FloatField(min_value=1, max_value=1000)
	sigma = forms.FloatField(min_value=0, max_value=0.9999)
	q = forms.FloatField(min_value=0, max_value=0.9999)
	r = forms.FloatField(min_value=0, max_value=0.9999)

class LegsForm(forms.Form): 
	position = forms.TypedChoiceField(choices=POSITION_CHOICES)
	kind = forms.TypedChoiceField(choices=KIND_CHOICES)
	K = forms.FloatField(min_value=1, max_value=1000)
	T = forms.FloatField(min_value=.00272, max_value=100)

