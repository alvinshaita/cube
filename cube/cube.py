import copy
import re

import numpy as np

from rubik.cubelet import Cubelet
from rubik.constants import SLICE


class Cube:
	def __init__(self, size=3, state=None):
		self.path = []
		self.size = size
		cube_state = state or "".join([i*(self.size**2) for i in "ybrgow"])
		self.state = cube_state.lower()

		assert(len(self.state) == (self.size**2)*6)
		self.cube_from_state()

	def set_state(self):
		orr = self.group_sides()
		self.state = "".join(["".join(i) for i in [ k[j] for k in [orr[ii] for ii in "ulfrbd"] for j in range(self.size)]])

	def __eq__(self, other):
		# only state determines equality, path does not
		return self.state == other.state

	def __repr__(self):
		return self.to_string()
		# return str(self.path)
		# return self.state

	def solved(self):
		grouped_solution = sorted([i*(self.size**2) for i in "ybrgow"])
		grouped_state = sorted(re.findall("."*(self.size**2), self.state))
		return grouped_solution == grouped_state

	def copy(self):
		return copy.deepcopy(self)

	def cube_from_state(self):
		self.cube = np.array([[[{} for k in range(self.size)] for j in range(self.size)] for i in range(self.size)])

		# reverse
		u_slice = [[self.state[(self.size**2)*0:(self.size**2)*1][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		u_slice = np.flipud(u_slice)

		l_slice = [[self.state[(self.size**2)*1:(self.size**2)*2][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		l_slice = np.rot90(l_slice, k=-1, axes=(1,0))

		f_slice = [[self.state[(self.size**2)*2:(self.size**2)*3][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		f_slice = np.array(f_slice)

		r_slice = [[self.state[(self.size**2)*3:(self.size**2)*4][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		r_slice = np.flipud(r_slice)
		r_slice = np.rot90(r_slice, k=-1)

		b_slice = [[self.state[(self.size**2)*4:(self.size**2)*5][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		b_slice = np.fliplr(b_slice)

		d_slice = [[self.state[(self.size**2)*5:(self.size**2)*6][self.size*i+j] for j in range(self.size)] for i in range(self.size)]
		d_slice = np.array(d_slice)


		# letter to name
		ltn = {"y": "yellow", "r": "red", "g": "green", "o": "orange", "b": "blue", "w": "white"}


		cc = [[[{} for k in range(self.size)] for j in range(self.size)] for i in range(self.size)]
		# print(cc)
		cc = np.array(cc)
		# uuu = cc[SLICE.U(0)]

		for i in range(len(u_slice)):
			for j in range(len(u_slice[i])):
				cc[SLICE.U(0)][i][j]["u"] = ltn[u_slice[i][j]]

		for i in range(len(l_slice)):
			for j in range(len(l_slice[i])):
				cc[SLICE.L(0)][i][j]["l"] = ltn[l_slice[i][j]]

		for i in range(len(f_slice)):
			for j in range(len(f_slice[i])):
				cc[SLICE.F(0)][i][j]["f"] = ltn[f_slice[i][j]]

		for i in range(len(r_slice)):
			for j in range(len(r_slice[i])):
				cc[SLICE.R(0)][i][j]["r"] = ltn[r_slice[i][j]]

		for i in range(len(b_slice)):
			for j in range(len(b_slice[i])):
				cc[SLICE.B(0)][i][j]["b"] = ltn[b_slice[i][j]]

		for i in range(len(d_slice)):
			for j in range(len(d_slice[i])):
				cc[SLICE.D(0)][i][j]["d"] = ltn[d_slice[i][j]]


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
				cube_slice[i][j].pos[l[0]], cube_slice[i][j].pos[l[1]], cube_slice[i][j].pos[l[2]], cube_slice[i][j].pos[l[3]] =\
				cube_slice[i][j].pos[r[0]], cube_slice[i][j].pos[r[1]], cube_slice[i][j].pos[r[2]], cube_slice[i][j].pos[r[3]]

	def rotate_u(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("u", times))
		cube_slice = self.cube[SLICE.U(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "lbrf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "lbrf", aaa)
		self.cube[SLICE.U(index_to_move)] = cube_slice
		self.set_state()

	def rotate_d(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("d", times))
		cube_slice = self.cube[SLICE.D(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "rflb"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "rflb", bbb)
		self.cube[SLICE.D(index_to_move)] = cube_slice
		self.set_state()

	def rotate_l(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("l", times))
		cube_slice = self.cube[SLICE.L(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "dfub"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "dfub", bbb)
		self.cube[SLICE.L(index_to_move)] = cube_slice
		self.set_state()

	def rotate_r(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("r", times))
		cube_slice = self.cube[SLICE.R(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "ubdf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "ubdf", aaa)
		self.cube[SLICE.R(index_to_move)] = cube_slice
		self.set_state()

	def rotate_f(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("f", times))
		cube_slice = self.cube[SLICE.F(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		aaa = "rdlu"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "rdlu", aaa)
		self.cube[SLICE.F(index_to_move)] = cube_slice
		self.set_state()

	def rotate_b(self, times_to_move=1, index_to_move=0):
		times = times_to_move%(3+1)
		self.path.append(("b", times))
		cube_slice = self.cube[SLICE.B(index_to_move)]
		cube_slice = np.rot90(cube_slice, k=times)

		bbb = "lurd"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "lurd", bbb)
		self.cube[SLICE.B(index_to_move)] = cube_slice
		self.set_state()

	def rotate_all_u(self, times_to_move=1):
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
