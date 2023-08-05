import numpy as np

U_SLICE = (slice(None), 0, slice(None))
D_SLICE = (slice(None), -1, slice(None))
L_SLICE = (slice(None), slice(None), 0)
R_SLICE = (slice(None), slice(None), -1)
F_SLICE = (0, slice(None), slice(None))
B_SLICE = (-1, slice(None), slice(None))


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
