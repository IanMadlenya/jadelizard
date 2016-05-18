from .option_models import Strategy

"""
Pre-configured Strategy Templates for the user to load. 
All are set with the following values: 
underlying price $100, volatility 25%, dividend yield 3%, risk-free rate 2%. 

Templates will be priced with the pricing model set in the session. 
"""

class LongCallSpread(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 95, 1)
		self.add_leg("short", "call", 105, 1)

class LongPutSpread(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 105, 1)

class ShortCallSpread(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("long", "call", 110, 1)

class ShortPutSpread(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 95, 1)

class LongCombination(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class ShortCombination(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class BackSpreadCalls(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "call", 105, 1)

class BackSpreadPuts(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 95, 1)
		self.add_leg("long", "put", 95, 1)

class FrontSpreadCalls(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "call", 105, 1)

class FrontSpreadPuts(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "put", 100, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("short", "put", 95, 1)

class LongStraddle(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class ShortStraddle(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class LongStrangle(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "put", 95, 1)

class ShortStrangle(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)

class LongCalendarSpreadCalls(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 100, .5)
		self.add_leg("long", "call", 100, 1)

class LongCalendarSpreadPuts(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "put", 100, .5)
		self.add_leg("long", "put", 100, 1)

class IronCondor(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 90, 1)

class IronButterfly(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 90, 1)

class JadeLizard(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("short", "call", 95, 1)
		self.add_leg("short", "put", 105, 1)
		self.add_leg("long", "call", 115, 1)

class DoubleDiagonal(Strategy): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100, .03, .02, .25)
		self.add_leg("long", "put", 90, .5)
		self.add_leg("short", "put", 96.5, .25)
		self.add_leg("short", "call", 104.5, .25)
		self.add_leg("long", "call", 110, .5)


Templates = {
	"LongCallSpread": LongCallSpread,
	"LongPutSpread": LongPutSpread,
	"ShortCallSpread": ShortCallSpread,
	"ShortPutSpread": ShortPutSpread,
	"LongCombination": LongCombination, 
	"ShortCombination": ShortCombination,
	"BackSpreadCalls": BackSpreadCalls, 
	"BackSpreadPuts": BackSpreadPuts, 
	"FrontSpreadCalls": FrontSpreadCalls, 
	"FrontSpreadPuts": FrontSpreadPuts,
	"LongStraddle": LongStraddle, 
	"LongStrangle": LongStrangle, 
	"ShortStraddle": ShortStraddle, 
	"ShortStrangle": ShortStrangle,
	"LongCalendarSpreadCalls": LongCalendarSpreadCalls, 
	"LongCalendarSpreadPuts": LongCalendarSpreadPuts, 
	"IronCondor": IronCondor,
	"IronButterfly": IronButterfly,
	"JadeLizard": JadeLizard, 
	"DoubleDiagonal": DoubleDiagonal
}









