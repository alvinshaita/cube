import numpy as np


cube_size = 4
arr_1d = np.arange(1, cube_size**3+1)
arr_3d = arr_1d.reshape(cube_size, cube_size, cube_size)

# Create a 3D array
# arr_3d = np.array([
#     [[1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]],
    
#     [[10, 11, 12],
#     [13, 14, 15],
#     [16, 17, 18]],
    
#     [[19, 20, 21],
#     [22, 23, 24],
#     [25, 26, 27]]
# ])

# Rotate the right side by 90 degrees
rotated_arr_3d = arr_3d.copy()  # Create a copy of the original array

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
rotated_right_side = np.rot90(right_side, k=1)

# Assign the rotated right side back to the array
rotated_arr_3d[:, :, -1] = rotated_right_side

print(rotated_arr_3d)
