from .option_models import Strategy


DEFAULT_S0 = 100
DEFAULT_q = .03
DEFAULT_r = .02
DEFAULT_sigma = .30

class Template(Strategy):
	def __init__(self, model_name): 
		super().__init__(model_name, DEFAULT_S0, DEFAULT_q, DEFAULT_r, DEFAULT_sigma)


"""
Strategies Involving a Stock Position
"""
class CoveredCall(Template):
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 105, 1)
		self.set_stock(1,0)

class MarriedPut(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 95, 1)
		self.set_stock(1,0)

class Collar(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "call", 110, 1)
		self.set_stock(1,0)


"""
Bullish Strategies
"""
class LongCall(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 100, 1)

class LongCallSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 95, 1)
		self.add_leg("short", "call", 105, 1)

class ShortPutSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 95, 1)

class LongCombination(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class BackSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 100, 0.25)
		self.add_leg("long", "call", 110, 0.25)
		self.add_leg("long", "call", 110, 0.25)

class FrontSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "call", 110, 1)
		self.add_leg("short", "call", 110, 1)

class BigLizard(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "call", 115, 1)

class JadeLizard(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 95, 1)
		self.add_leg("short", "put", 105, 1)
		self.add_leg("long", "call", 115, 1)


"""
Bearish Strategies
"""	
class LongPut(Template): 
	def __init__(self, model_name):
		super().__init__(model_name)
		self.add_leg("long", "put", 100, 1)

class LongPutSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 105, 1)

class ShortCallSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("long", "call", 110, 1)

class ShortCombination(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class BackSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "put", 110, 0.25)
		self.add_leg("long", "put", 100, 0.25)
		self.add_leg("long", "put", 100, 0.25)

class FrontSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 100, 1)
		self.add_leg("short", "put", 90, 1)
		self.add_leg("short", "put", 90, 1)


"""
Non-Directional Strategies: Low Volatility
"""
class ShortStraddle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class ShortStrangle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)

class LongCalendarSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 100, .5)
		self.add_leg("long", "call", 100, 1)

class LongCalendarSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "put", 100, .5)
		self.add_leg("long", "put", 100, 1)

class DoubleDiagonal(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 90, .5)
		self.add_leg("short", "put", 96.5, .25)
		self.add_leg("short", "call", 104.5, .25)
		self.add_leg("long", "call", 110, .5)


"""
Condor
"""
class LongCondorCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 90, 1)
		self.add_leg("short", "call", 95, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("long", "call", 110, 1)

class LongCondorPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("short", "put", 105, 1)
		self.add_leg("long", "put", 110, 1)

class IronCondor(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 90, 1)

class IronAlbatross(Template):
	def __init__(self, model_name):
		super().__init__(model_name)
		self.add_leg("long", "call", 130,1)
		self.add_leg("short", "call", 120, 1)
		self.add_leg("short", "put", 80, 1)
		self.add_leg("long", "put", 70, 1)


"""
Butterfly
"""
class LongButterflyCalls(Template): 
	def __init__(self, model_name):
		super().__init__(model_name)
		self.add_leg("long", "call", 90, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "call", 110, 1)

class LongButterflyPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 110, 1)

class IronButterfly(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 90, 1)


"""
Non-Directional Strategies: High Volatility
"""
class LongStraddle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class LongStrangle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "put", 95, 1)

class ReverseIronButterfly(Template):
	def __init__(self, model_name):
		super().__init__(model_name)
		self.add_leg("short", "call", 110, 1)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)
		self.add_leg("short", "put", 90, 1)

class ReverseIronCondor(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 110, 1)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "put", 95, 1)
		self.add_leg("short", "put", 90, 1)

class ReverseIronAlbatross(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name)
		self.add_leg("short", "call", 130, 1)
		self.add_leg("long", "call", 120, 1)
		self.add_leg("long", "put", 80, 1)
		self.add_leg("short", "put", 70, 1)





Templates = {
	"CoveredCall": CoveredCall, 
	"MarriedPut": MarriedPut,
	"Collar":Collar,
	"LongCall":LongCall,
	"LongCallSpread": LongCallSpread,
	"ShortPutSpread": ShortPutSpread,
	"LongCombination": LongCombination, 
	"BackSpreadCalls": BackSpreadCalls, 
	"FrontSpreadCalls": FrontSpreadCalls, 
	"BigLizard": BigLizard,
	"JadeLizard": JadeLizard, 
	"LongPut":LongPut,
	"LongPutSpread": LongPutSpread,
	"ShortCallSpread": ShortCallSpread,
	"ShortCombination": ShortCombination,
	"BackSpreadPuts": BackSpreadPuts, 
	"FrontSpreadPuts": FrontSpreadPuts,
	"ShortStraddle": ShortStraddle, 
	"ShortStrangle": ShortStrangle,
	"LongCalendarSpreadCalls": LongCalendarSpreadCalls, 
	"LongCalendarSpreadPuts": LongCalendarSpreadPuts, 
	"DoubleDiagonal": DoubleDiagonal,
	"LongCondorCalls": LongCondorCalls, 
	"LongCondorPuts": LongCondorPuts,
	"IronCondor": IronCondor,
	"IronAlbatross": IronAlbatross,
	"LongButterflyCalls": LongButterflyCalls, 
	"LongButterflyPuts": LongButterflyPuts,
	"IronButterfly": IronButterfly,
	"LongStraddle": LongStraddle, 
	"LongStrangle": LongStrangle,
	"ReverseIronButterfly": ReverseIronButterfly,
	"ReverseIronCondor": ReverseIronCondor,
	"ReverseIronAlbatross": ReverseIronAlbatross 
}




