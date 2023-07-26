import numpy as np


# a = []

class One:
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return str(self.value)



class Two:
	def __init__(self, size=3):
		self.size = size
		arr_1d = np.array([One(i) for i in range(1, self.size**3+1)])
		arr_3d = arr_1d.reshape(self.size, self.size, self.size)
		self.array = arr_3d

	def rotate_right(self, times=1):
		# Rotate the right side by 90 degrees
		rotated_arr_3d = self.array.copy()  # Create a copy of the original array

		# Get the right side of the array
		right_side = rotated_arr_3d[:, :, -1]


		# top_side = rotated_arr_3d[0, :, :]
		# front_side = rotated_arr_3d[:, 0, :]
		# right_side = rotated_arr_3d[:, :, 0]

		# right_side = rotated_arr_3d[:, :, 0]
		# right_side = rotated_arr_3d[:, :, 1]
		# right_side = rotated_arr_3d[:, :, 2]

		# print(top_side)
		# # Rotate the right side by 90 degrees
		rotated_right_side = np.rot90(right_side, k=times)

		# Assign the rotated right side back to the array
		rotated_arr_3d[:, :, -1] = rotated_right_side

		# print(rotated_arr_3d)
		self.array = rotated_arr_3d


	# def rotate_right(self, times=1):
	# 	# Rotate the right side by 90 degrees
	# 	rotated_arr_3d = self.array.copy()  # Create a copy of the original array

	# 	# Get the right side of the array
	# 	right_side = rotated_arr_3d[:, :, -1]


	# 	# top_side = rotated_arr_3d[0, :, :]
	# 	# front_side = rotated_arr_3d[:, 0, :]
	# 	# right_side = rotated_arr_3d[:, :, 0]

	# 	# right_side = rotated_arr_3d[:, :, 0]
	# 	# right_side = rotated_arr_3d[:, :, 1]
	# 	# right_side = rotated_arr_3d[:, :, 2]

	# 	# print(top_side)
	# 	# # Rotate the right side by 90 degrees
	# 	rotated_right_side = np.rot90(right_side, k=times)

	# 	# Assign the rotated right side back to the array
	# 	rotated_arr_3d[:, :, -1] = rotated_right_side

	# 	# print(rotated_arr_3d)
	# 	self.array = rotated_arr_3d

















	# def rot90(self):
	# 	# Rotate the right side by 90 degrees
	# 	rotated_arr_3d = self.array.copy()  # Create a copy of the original array

	# 	# Get the right side of the array
	# 	right_side = rotated_arr_3d[:, :, -1]


	# 	# top_side = rotated_arr_3d[0, :, :]
	# 	# front_side = rotated_arr_3d[:, 0, :]
	# 	# right_side = rotated_arr_3d[:, :, 0]

	# 	# right_side = rotated_arr_3d[:, :, 0]
	# 	# right_side = rotated_arr_3d[:, :, 1]
	# 	# right_side = rotated_arr_3d[:, :, 2]

	# 	# print(top_side)
	# 	# # Rotate the right side by 90 degrees
	# 	rotated_right_side = np.rot90(right_side, k=1)

	# 	# Assign the rotated right side back to the array
	# 	rotated_arr_3d[:, :, -1] = rotated_right_side

	# 	# print(rotated_arr_3d)
	# 	self.array = rotated_arr_3d

	def __repr__(self):
		return str(self.array)

t = Two(3)
print(t)
t.rotate_right()
print("=======================")
print(t)
t.rotate_right()
print("=======================")
print(t)
t.rotate_right()
print("=======================")
print(t)
t.rotate_right()
print("=======================")
print(t)
