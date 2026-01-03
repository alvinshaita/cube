import copy
import random
import re

import numpy as np

from .cubelet import Cubelet
from .constants import SLICE
from .solver.utils import solve as solve_from_state

class Cube:
	def __init__(self, size=3, state=None):
		self.path = []
		self.size = size

		self.default_state = "".join([i*(self.size**2) for i in "ybrgow"]).lower()
		self.state = state.lower() if state else self.default_state

		assert(len(self.state) == (self.size**2)*6)
		self.generate_cube()

	def load_state(self):
		orr = self.group_sides()
		raw_state = [
			"".join(i)
			for i in [
				k[j]
				for k in [orr[ii] for ii in "ulfrbd"]
				for j in range(self.size)
			]
		]
		self.state = "".join(raw_state)

	def __eq__(self, other):
		# only state determines equality, path does not
		return self.state == other.state

	def __repr__(self):
		return self.to_string()
		# return str(self.path)
		# return self.state

	def solve(self, method="kociemba"):
		solution_moves = solve_from_state(self.state, "kociemba")
		solution = " ".join([str(move) for move in solution_moves])
		return solution

	def solved(self):
		grouped_solution = sorted([i*(self.size**2) for i in "ybrgow"])
		grouped_state = sorted(re.findall("."*(self.size**2), self.state))
		return grouped_solution == grouped_state

	def copy(self):
		return copy.deepcopy(self)

	# generates a cube array from the state
	# each item is a Cubelet
	def generate_cube(self):
		"""
		Generate a cube. A 3 dimension array holding each piece of the cube
		"""
		# create array of NxNxN
		self.cube = np.array([[[
			{}
			for _ in range(self.size)]
			for _ in range(self.size)]
			for _ in range(self.size)]
		)

		# group each face of the cube
		# reverse
		u_slice = [[
			self.state[(self.size**2)*0 : (self.size**2)*1][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		u_slice = np.flipud(u_slice)

		l_slice = [[
			self.state[(self.size**2)*1 : (self.size**2)*2][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		l_slice = np.rot90(l_slice, k=-1, axes=(1,0))

		f_slice = [[
			self.state[(self.size**2)*2 : (self.size**2)*3][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		f_slice = np.array(f_slice)

		r_slice = [[
			self.state[(self.size**2)*3 : (self.size**2)*4][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		r_slice = np.flipud(r_slice)
		r_slice = np.rot90(r_slice, k=-1)

		b_slice = [[
			self.state[(self.size**2)*4 : (self.size**2)*5][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		b_slice = np.fliplr(b_slice)

		d_slice = [[
			self.state[(self.size**2)*5 : (self.size**2)*6][self.size*i+j]
			for j in range(self.size)]
			for i in range(self.size)]
		d_slice = np.array(d_slice)


		# letter to map to color name
		color_map = {"y": "yellow", "r": "red", "g": "green", "o": "orange", "b": "blue", "w": "white"}

		cc = [[[
			{}
			for _ in range(self.size)]
			for _ in range(self.size)]
			for _ in range(self.size)]
		cc = np.array(cc)

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.U(0)] [i] [j] ["u"] = color_map[ u_slice[i][j] ]

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.L(0)] [i] [j] ["l"] = color_map[ l_slice[i][j] ]

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.F(0)] [i] [j] ["f"] = color_map[ f_slice[i][j] ]

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.R(0)] [i] [j] ["r"] = color_map[ r_slice[i][j] ]

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.B(0)] [i] [j] ["b"] = color_map[ b_slice[i][j] ]

		for i in range(self.size):
			for j in range(self.size):
				cc[SLICE.D(0)] [i] [j] ["d"] = color_map[ d_slice[i][j] ]


		for i in range(self.size):
			for j in range(self.size):
				for k in range(self.size):
					for kk in "ulfrbd":
						if not cc[i][j][k].get(kk):
							cc[i][j][k][kk] = None
					self.cube[i][j][k] = Cubelet(cc[i][j][k])

	def orient_cubelets(self, cube_slice, l, r):
		# cubelets are on the correct spot but not facing the correct direction,
		# so we orient them correctly
		for i in range(len(cube_slice)):
			for j in range(len(cube_slice[i])):
				cube_slice [i] [j] .pos[ l[0] ], \
				cube_slice [i] [j] .pos[ l[1] ], \
				cube_slice [i] [j] .pos[ l[2] ], \
				cube_slice [i] [j] .pos[ l[3] ] = \
				cube_slice [i] [j] .pos[ r[0] ], \
				cube_slice [i] [j] .pos[ r[1] ], \
				cube_slice [i] [j] .pos[ r[2] ], \
				cube_slice [i] [j] .pos[ r[3] ]

	# rotate up
	def rotate_u(self, times_to_move=1, index_to_move=0):
		"""
		Rotate up slice
			- times_to_move: The number of times to rotate the slice
								+ve values rotates clockwise
								-ve values rotates anticlockwise
			- index_to_move: The slice index to move
								0 rotates only the top most slice
								1 rotates only the second slice
		"""
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("u", times))
		cube_slice = self.cube[SLICE.U(index)]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "lbrf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "lbrf", aaa)
		self.cube[SLICE.U(index)] = cube_slice
		self.load_state()

	def rotate_d(self, times_to_move=1, index_to_move=0):
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("d", times))
		cube_slice = self.cube[SLICE.D(index)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "rflb"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "rflb", bbb)
		self.cube[SLICE.D(index)] = cube_slice
		self.load_state()

	def rotate_l(self, times_to_move=1, index_to_move=0):
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("l", times))
		cube_slice = self.cube[SLICE.L(index)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "dfub"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "dfub", bbb)
		self.cube[SLICE.L(index)] = cube_slice
		self.load_state()

	def rotate_r(self, times_to_move=1, index_to_move=0):
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("r", times))
		cube_slice = self.cube[SLICE.R(index)]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "ubdf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "ubdf", aaa)
		self.cube[SLICE.R(index)] = cube_slice
		self.load_state()

	def rotate_f(self, times_to_move=1, index_to_move=0):
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("f", times))
		cube_slice = self.cube[SLICE.F(index)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		aaa = "rdlu"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "rdlu", aaa)
		self.cube[SLICE.F(index)] = cube_slice
		self.load_state()

	def rotate_b(self, times_to_move=1, index_to_move=0):
		times = times_to_move % (3+1)
		index = index_to_move
		self.path.append(("b", times))
		cube_slice = self.cube[SLICE.B(index)]
		cube_slice = np.rot90(cube_slice, k=times)

		bbb = "lurd"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "lurd", bbb)
		self.cube[SLICE.B(index)] = cube_slice
		self.load_state()

	def rotate(self, moves):
		moves = moves.lower()
		moves = moves.split(" ")
		for move in moves:
			if move == "u":
				self.rotate_u()
			elif move == "u'":
				self.rotate_u(times_to_move=-1)
			elif move == "u2":
				self.rotate_u(times_to_move=2)
			elif move == "l":
				self.rotate_l()
			elif move == "l'":
				self.rotate_l(times_to_move=-1)
			elif move == "l2":
				self.rotate_l(times_to_move=2)
			elif move == "f":
				self.rotate_f()
			elif move == "f'":
				self.rotate_f(times_to_move=-1)
			elif move == "f2":
				self.rotate_f(times_to_move=2)
			elif move == "r":
				self.rotate_r()
			elif move == "r'":
				self.rotate_r(times_to_move=-1)
			elif move == "r2":
				self.rotate_r(times_to_move=2)
			elif move == "b":
				self.rotate_b()
			elif move == "b'":
				self.rotate_b(times_to_move=-1)
			elif move == "b2":
				self.rotate_b(times_to_move=2)
			elif move == "d":
				self.rotate_d()
			elif move == "d'":
				self.rotate_d(times_to_move=-1)
			elif move == "d2":
				self.rotate_d(times_to_move=2)

	def rotate_all_u(self, times_to_move=1):
		# basically changing the orientation of the cube
		# rotating each slice of the cube the number of times specified
		for i in range(self.size):
			self.rotate_u(times_to_move=times_to_move, index_to_move=i)

	def rotate_all_d(self, times_to_move=1):
		for i in range(self.size):
			self.rotate_d(times_to_move=times_to_move, index_to_move=i)

	def rotate_all_l(self, times_to_move=1):
		for i in range(self.size):
			self.rotate_l(times_to_move=times_to_move, index_to_move=i)

	def rotate_all_r(self, times_to_move=1):
		for i in range(self.size):
			self.rotate_r(times_to_move=times_to_move, index_to_move=i)

	def rotate_all_f(self, times_to_move=1):
		for i in range(self.size):
			self.rotate_f(times_to_move=times_to_move, index_to_move=i)

	def rotate_all_b(self, times_to_move=1):
		for i in range(self.size):
			self.rotate_b(times_to_move=times_to_move, index_to_move=i)

	def group_sides(self):
		# group sides based on direction and in an order that is easily comprehesible in 2d representation
		orr = {"f": [], "b": [], "u": [], "d": [], "l": [], "r": []}

		# name to letter
		# ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w", None: " "}
		ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w"}


		f_slice = self.cube[SLICE.F(0)]
		orr["f"] = [[ntl[f.pos["f"]] for f in ff] for ff in f_slice]

		b_slice = self.cube[SLICE.B(0)]
		b_slice = np.fliplr(b_slice)
		orr["b"] = [[ntl[b.pos["b"]] for b in bb] for bb in b_slice]

		u_slice = self.cube[SLICE.U(0)]
		u_slice = np.flipud(u_slice)
		orr["u"] = [[ntl[u.pos["u"]] for u in uu] for uu in u_slice]

		d_slice = self.cube[SLICE.D(0)]
		orr["d"] = [[ntl[d.pos["d"]] for d in dd] for dd in d_slice]

		l_slice = self.cube[SLICE.L(0)]
		l_slice = np.rot90(l_slice, k=1, axes=(1,0))
		orr["l"] = [[ntl[l.pos["l"]] for l in ll] for ll in l_slice]

		r_slice = self.cube[SLICE.R(0)]
		r_slice = np.rot90(r_slice, k=1)
		r_slice = np.flipud(r_slice)
		orr["r"] = [[ntl[r.pos["r"]] for r in rr] for rr in r_slice]

		return orr

	def to_string(self):
		"""
		Returns a string representation of the cube
		"""
		rep = ""
		for i in range(self.size):
			rep += " "*(self.size+1) + "|"
			rep += self.state[i*self.size:(i+1)*self.size]
			rep += "|\n"
		for i in range(self.size):
			rep += "|"
			rep += "|".join([self.state[(self.size+i+self.size*j)*self.size:(self.size+i+self.size*j+1)*self.size] for j in range(4)])
			rep += "|\n"
		for i in range(self.size):
			rep += " "*(self.size+1) + "|"
			rep += self.state[(i+(self.size*5))*self.size:(i+(self.size*5)+1)*self.size]
			rep += "|\n"
		return rep
