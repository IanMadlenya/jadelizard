from django import forms 

POSITION_CHOICES=[
("long", "long"),
("short", "short")
]

KIND_CHOICES=[
("call", "call"), 
("put", "put")
]

MODEL_CHOICES=[
("BlackScholes", "BlackScholes"),
("BinomialTree", "BinomialTree")
]

EXER_CHOICES=[
("european", "european"),
("american", "american")
]

STEPS_CHOICES=[
("10",10),
("25",25),
("50",50)
]

class NewStrategyForm(forms.Form):
	S0 = forms.FloatField(min_value=1, max_value=1000)
	sigma = forms.FloatField(min_value=0, max_value=0.9999)
	q = forms.FloatField(min_value=0, max_value=0.9999)
	r = forms.FloatField(min_value=0, max_value=0.9999)

class LegsForm(forms.Form): 
	position = forms.ChoiceField(choices=POSITION_CHOICES)
	kind = forms.ChoiceField(choices=KIND_CHOICES)
	K = forms.FloatField(min_value=1, max_value=1000)
	T = forms.FloatField(min_value=.01, max_value=20)

class PriceModelForm(forms.Form): 
	model = forms.ChoiceField(choices=MODEL_CHOICES)
	exer_type = forms.ChoiceField(choices=EXER_CHOICES)
	steps = forms.ChoiceField(choices=STEPS_CHOICES)



