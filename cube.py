import numpy as np
from constants import SLICE, DEFAULT_STATE
from cubelet import Cubelet

class Cube:
	def __init__(self, state=DEFAULT_STATE):
		assert(len(state) == 3*3*6)
		self.state = state
		self.cube_from_state()

		# get the center color from each face
		self.state[9//2::9]
		self.solution = "".join([i*9 for i in self.state[9//2::9]])
		assert(len(self.solution) == 3*3*6)

	def cube_from_state(self):
		self.cube = np.array([[[{} for k in range(3)] for j in range(3)] for i in range(3)])

		# reverse
		u_slice = [[self.state[9*0:9*1][3*i+j] for j in range(3)] for i in range(3)]
		u_slice = np.flipud(u_slice)

		l_slice = [[self.state[9*1:9*2][3*i+j] for j in range(3)] for i in range(3)]
		l_slice = np.rot90(l_slice, k=-1, axes=(1,0))

		f_slice = [[self.state[9*2:9*3][3*i+j] for j in range(3)] for i in range(3)]
		f_slice = np.array(f_slice)

		r_slice = [[self.state[9*3:9*4][3*i+j] for j in range(3)] for i in range(3)]
		r_slice = np.flipud(r_slice)
		r_slice = np.rot90(r_slice, k=-1)

		b_slice = [[self.state[9*4:9*5][3*i+j] for j in range(3)] for i in range(3)]
		b_slice = np.fliplr(b_slice)

		d_slice = [[self.state[9*5:9*6][3*i+j] for j in range(3)] for i in range(3)]
		d_slice = np.array(d_slice)


		# letter to name
		ltn = {"y": "yellow", "r": "red", "g": "green", "o": "orange", "b": "blue", "w": "white"}


		cc = [[[{} for k in range(3)] for j in range(3)] for i in range(3)]
		# print(cc)
		cc = np.array(cc)
		# uuu = cc[SLICE.U]

		for i in range(len(u_slice)):
			for j in range(len(u_slice[i])):
				cc[SLICE.U][i][j]["u"] = ltn[u_slice[i][j]]

		for i in range(len(l_slice)):
			for j in range(len(l_slice[i])):
				cc[SLICE.L][i][j]["l"] = ltn[l_slice[i][j]]

		for i in range(len(f_slice)):
			for j in range(len(f_slice[i])):
				cc[SLICE.F][i][j]["f"] = ltn[f_slice[i][j]]

		for i in range(len(r_slice)):
			for j in range(len(r_slice[i])):
				cc[SLICE.R][i][j]["r"] = ltn[r_slice[i][j]]

		for i in range(len(b_slice)):
			for j in range(len(b_slice[i])):
				cc[SLICE.B][i][j]["b"] = ltn[b_slice[i][j]]

		for i in range(len(d_slice)):
			for j in range(len(d_slice[i])):
				cc[SLICE.D][i][j]["d"] = ltn[d_slice[i][j]]


		for i in range(3):
			for j in range(3):
				for k in range(3):
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

	def rotate_u(self, times=1):
		cube_slice = self.cube[SLICE.U]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "lbrf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "lbrf", aaa)
		self.cube[SLICE.U] = cube_slice
		self.set_state()

	def rotate_d(self, times=1):
		cube_slice = self.cube[SLICE.D]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "rflb"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "rflb", bbb)
		self.cube[SLICE.D] = cube_slice
		self.set_state()

	def rotate_l(self, times=1):
		cube_slice = self.cube[SLICE.L]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		bbb = "dfub"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "dfub", bbb)
		self.cube[SLICE.L] = cube_slice
		self.set_state()

	def rotate_r(self, times=1):
		cube_slice = self.cube[SLICE.R]
		cube_slice = np.rot90(cube_slice, k=times)

		aaa = "ubdf"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "ubdf", aaa)
		self.cube[SLICE.R] = cube_slice
		self.set_state()

	def rotate_f(self, times=1):
		cube_slice = self.cube[SLICE.F]
		cube_slice = np.rot90(cube_slice, k=times, axes=(1,0))

		aaa = "rdlu"
		for i in range(times):
			aaa = aaa[-1] + aaa[:3]

		self.orient_cubelets(cube_slice, "rdlu", aaa)
		self.cube[SLICE.F] = cube_slice
		self.set_state()

	def rotate_b(self, times=1):
		cube_slice = self.cube[SLICE.B]
		cube_slice = np.rot90(cube_slice, k=times)

		bbb = "lurd"
		for i in range(times):
			bbb = bbb[1:] + bbb[0]

		self.orient_cubelets(cube_slice, "lurd", bbb)
		self.cube[SLICE.B] = cube_slice
		self.set_state()

	def set_state(self):
		orr = self.group_sides()
		self.state = "".join(["".join(i) for i in [ k[j] for k in [orr[ii] for ii in "ulfrbd"] for j in range(3)]])



	def group_sides(self):
		# group sides based on direction and in an order that is easily comprehesible in 2d representation
		orr = {"f": [], "b": [], "u": [], "d": [], "l": [], "r": []}

		# name to letter
		# ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w", None: " "}
		ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w"}


		f_slice = self.cube[SLICE.F]
		orr["f"] = [[ntl[f.pos["f"]] for f in ff] for ff in f_slice]

		b_slice = self.cube[SLICE.B]
		b_slice = np.fliplr(b_slice)
		orr["b"] = [[ntl[b.pos["b"]] for b in bb] for bb in b_slice]

		u_slice = self.cube[SLICE.U]
		u_slice = np.flipud(u_slice)
		orr["u"] = [[ntl[u.pos["u"]] for u in uu] for uu in u_slice]

		d_slice = self.cube[SLICE.D]
		orr["d"] = [[ntl[d.pos["d"]] for d in dd] for dd in d_slice]

		l_slice = self.cube[SLICE.L]
		l_slice = np.rot90(l_slice, k=1, axes=(1,0))
		orr["l"] = [[ntl[l.pos["l"]] for l in ll] for ll in l_slice]

		r_slice = self.cube[SLICE.R]
		r_slice = np.rot90(r_slice, k=1)
		r_slice = np.flipud(r_slice)
		orr["r"] = [[ntl[r.pos["r"]] for r in rr] for rr in r_slice]

		return orr

	def __repr__(self):
		rep = ""
		for i in range(3):
			rep += " "*(3+1) + "|"
			rep += self.state[i*3:(i+1)*3]
			rep += "|\n"
		for i in range(3):
			rep += "|"
			rep += "|".join([self.state[(3+i+3*j)*3:(3+i+3*j+1)*3] for j in range(4)])
			rep += "|\n"
		for i in range(3):
			rep += " "*(3+1) + "|"
			rep += self.state[(i+15)*3:(i+16)*3]
			rep += "|\n"
		return rep




# state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
state = "oggoyrbbryyrbbbwwwyrgyrwbrwyyoggwggwyyboowoogrgorworbb"
# c = Cube(state)
c = Cube()

# print(c.state)
# c.rotate_f(5)
# c.rotate_r(5)
# c.rotate_b(5)
# c.rotate_l(5)


# default_state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
print(c.state)
# print(c)
c.set_state()
print(c.solution)