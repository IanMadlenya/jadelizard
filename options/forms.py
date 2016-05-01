from django import forms 


class NewStrategyForm(forms.Form): 

	class Meta: 

		fields = ["S0"]

class LegsForm(forms.Form): 

	class Meta: 

		fields= ["K"]