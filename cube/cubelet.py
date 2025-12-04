import numpy as np

class Cubelet:
	def __init__(self, pos):
		self.pos = pos
		# self.u = pos.get("u")
		# self.d = pos.get("d")
		# self.l = pos.get("l")
		# self.r = pos.get("r")
		# self.f = pos.get("f")
		# self.b = pos.get("b")

	def __repr__(self):
		return str(self.pos)
