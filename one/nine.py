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


DEFAULT_CUBE = [
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": "red", "b": None})
		],

		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": "red", "b": None})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": "red", "b": None}),
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": "red", "b": None})
			]
	],
	
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": None})
		],

		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": None, "b": None})
		],

		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": None, "b": None}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": None})
		]
	],
	
	[
		[
			Cubelet({"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": "orange"})
		],
		
		[
			Cubelet({"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": None, "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": None, "l": None, "r": "green", "f": None, "b": "orange"})
		],
		
		[
			Cubelet({"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": None, "f": None, "b": "orange"}), 
			Cubelet({"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": "orange"})
		]
	]
]




class Cube:
	def __init__(self):
		self.cube = np.array(DEFAULT_CUBE)

	def orient_cubelets(self, cube_slice, l, r):
		# cubelets are on the correct spot but not facing the correct direction,
		# so we orient them correctly
		for i in range(len(cube_slice)):
			for j in range(len(cube_slice[i])):
				cube_slice[i][j].pos[l[0]], cube_slice[i][j].pos[l[1]], cube_slice[i][j].pos[l[2]], cube_slice[i][j].pos[l[3]] =\
				cube_slice[i][j].pos[r[0]], cube_slice[i][j].pos[r[1]], cube_slice[i][j].pos[r[2]], cube_slice[i][j].pos[r[3]]

	def rotate_u(self, k=1):
		cube_slice = self.cube[U_SLICE]
		cube_slice = np.rot90(cube_slice, k=k)
		self.orient_cubelets(cube_slice, "lbrf", "flbr")
		self.cube[U_SLICE] = cube_slice

	def rotate_d(self, k=1):
		cube_slice = self.cube[D_SLICE]
		cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
		self.orient_cubelets(cube_slice, "rflb", "flbr")
		self.cube[D_SLICE] = cube_slice

	def rotate_l(self, k=1):
		cube_slice = self.cube[L_SLICE]
		cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
		self.orient_cubelets(cube_slice, "dfub", "fubd")
		self.cube[L_SLICE] = cube_slice

	def rotate_r(self, k=1):
		cube_slice = self.cube[R_SLICE]
		cube_slice = np.rot90(cube_slice, k=k)
		self.orient_cubelets(cube_slice, "ubdf", "fubd")
		self.cube[R_SLICE] = cube_slice

	def rotate_f(self, k=1):
		cube_slice = self.cube[F_SLICE]
		cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
		self.orient_cubelets(cube_slice, "rdlu", "urdl")
		self.cube[F_SLICE] = cube_slice

	def rotate_b(self, k=1):
		cube_slice = self.cube[B_SLICE]
		cube_slice = np.rot90(cube_slice, k=k)
		self.orient_cubelets(cube_slice, "lurd", "urdl")
		self.cube[B_SLICE] = cube_slice



	def group_sides(self):
		# group sides based on direction and in an order that is easily comprehesible in 2d representation
		orr = {"f": [], "b": [], "u": [], "d": [], "l": [], "r": []}

		f_slice = self.cube[F_SLICE]
		orr["f"] = [[f.pos["f"] for f in ff] for ff in f_slice]

		b_slice = self.cube[B_SLICE]
		b_slice = np.fliplr(b_slice)
		orr["b"] = [[b.pos["b"] for b in bb] for bb in b_slice]

		u_slice = self.cube[U_SLICE]
		u_slice = np.flipud(u_slice)
		orr["u"] = [[u.pos["u"] for u in uu] for uu in u_slice]

		d_slice = self.cube[D_SLICE]
		orr["d"] = [[d.pos["d"] for d in dd] for dd in d_slice]

		l_slice = self.cube[L_SLICE]
		l_slice = np.rot90(l_slice, k=1, axes=(1,0))
		orr["l"] = [[l.pos["l"] for l in ll] for ll in l_slice]

		r_slice = self.cube[R_SLICE]
		r_slice = np.rot90(r_slice, k=1)
		r_slice = np.flipud(r_slice)
		orr["r"] = [[r.pos["r"] for r in rr] for rr in r_slice]

		return orr

	def __repr__(self):
		orr = self.group_sides()

		# name to letter
		ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w", None: " "}

		rep = ""
		for i in range(3):
			rep += " "
			rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["u"]]])
			rep += "|\n"        
		for i in range(3):
			rep += "|"
			rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [orr["l"], orr["f"], orr["r"], orr["b"]]])
			rep += "|\n"
		for i in range(3):
			rep += " "
			rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["d"]]])
			rep += "|\n"

		return rep







c = Cube()

c.rotate_f()
c.rotate_r()
c.rotate_b()
c.rotate_l()

print(c)
