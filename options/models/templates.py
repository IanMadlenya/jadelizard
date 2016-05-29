from .option_models import Strategy


DEFAULT_q = .03
DEFAULT_r = .02
DEFAULT_sigma = .30

class Template(Strategy):
	def __init__(self, model_name, S0): 
		super().__init__(model_name, S0, DEFAULT_q, DEFAULT_r, DEFAULT_sigma)



class LongCallSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 95, 1)
		self.add_leg("short", "call", 105, 1)

class LongPutSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 105, 1)

class ShortCallSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("long", "call", 110, 1)

class ShortPutSpread(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 95, 1)

class LongCombination(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class ShortCombination(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class BackSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "call", 105, 1)

class BackSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 95, 1)
		self.add_leg("long", "put", 95, 1)

class FrontSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "call", 105, 1)

class FrontSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "put", 100, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("short", "put", 95, 1)

class LongStraddle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 100, 1)
		self.add_leg("long", "put", 100, 1)

class ShortStraddle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)

class LongStrangle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 105, 1)
		self.add_leg("long", "put", 95, 1)

class ShortStrangle(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)

class LongCalendarSpreadCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 100, .5)
		self.add_leg("long", "call", 100, 1)

class LongCalendarSpreadPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "put", 100, .5)
		self.add_leg("long", "put", 100, 1)

class LongCondorCalls(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 90, 1)
		self.add_leg("short", "call", 95, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("long", "call", 110)

class LongCondorPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("short", "put", 105, 1)
		self.add_leg("long", "put", 110, 1)

class IronCondor(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 105, 1)
		self.add_leg("short", "put", 95, 1)
		self.add_leg("long", "put", 90, 1)

class LongButterflyCalls(Template): 
	def __init__(self, model_name):
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 90, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("long", "call", 110, 1)

class LongButterflyPuts(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "put", 90, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 110, 1)

class IronButterfly(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("long", "call", 110, 1)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "put", 90, 1)

class JadeLizard(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 95, 1)
		self.add_leg("short", "put", 105, 1)
		self.add_leg("long", "call", 115, 1)

class BigLizard(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
		self.add_leg("short", "call", 100, 1)
		self.add_leg("short", "put", 100, 1)
		self.add_leg("long", "call", 115, 1)

class DoubleDiagonal(Template): 
	def __init__(self, model_name): 
		super().__init__(model_name, 100)
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
	"LongCondorCalls": LongCondorCalls, 
	"LongCondorPuts": LongCondorPuts,
	"IronCondor": IronCondor,
	"LongButterflyCalls": LongButterflyCalls, 
	"LongButterflyPuts": LongButterflyPuts,
	"IronButterfly": IronButterfly,
	"JadeLizard": JadeLizard, 
	"BigLizard": BigLizard,
	"DoubleDiagonal": DoubleDiagonal
}









