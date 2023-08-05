import numpy as np

# Create a 3D array
arr_3d = np.array([
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    [[19, 20, 21], [22, 23, 24], [25, 26, 27]]
])

# Rotate the right side by 90 degrees
rotated_arr_3d = arr_3d.copy()  # Create a copy of the original array

# Get the right side of the array
right_side = rotated_arr_3d[:, :, -1]

# Rotate the right side by 90 degrees
rotated_right_side = np.rot90(right_side, k=1)

# Assign the rotated right side back to the array
rotated_arr_3d[:, :, -1] = rotated_right_side

print(rotated_arr_3d)
