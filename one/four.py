import numpy as np


arr = np.array([
    [[1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]],
    
    [[10, 11, 12],
    [13, 14, 15],
    [16, 17, 18]],
    
    [[19, 20, 21],
    [22, 23, 24],
    [25, 26, 27]]
])



def rotate_right(arr):
    r=2
    aaa = arr[:, :, r]
    aaa = np.rot90(aaa, k=1)
    arr[:, :, r] = aaa

def rotate_left(arr):
    r=0
    aaa = arr[:, :, r]
    aaa = np.rot90(aaa, k=1)
    arr[:, :, r] = aaa

def rotate_front(arr):
    r=0
    aaa = arr[r, :, :]
    aaa = np.rot90(aaa, k=1)
    arr[r, :, :] = aaa

def rotate_back(arr):
    r=0
    aaa = arr[:, :, r]
    aaa = np.rot90(aaa, k=1)
    arr[:, :, r] = aaa





print(arr)
print("=============================")

# aaa = arr[:, :, -1]
# # bbb = np.rot90(aaa, k=1)
# # arr[:, :, -1] = bbb




# print(aaa)
print(arr[0, :, :])
print(np.rot90(arr[0, :, :], k=1))


# arr[:, :, -1] = aaa


# rotate_right(arr)
# rotate_left(arr)
rotate_front(arr)

print("=============================")
print(arr)













# import numpy as np


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

# print(arr_3d)
# print("=============================")

# # rotated_arr_3d = arr_3d.copy()

# # Get the right side of the array
# right_side = arr_3d[:, :, -1]

# # print(right_side)
# print(arr_3d[:, :, :])




# # top_side = arr_3d[0, :, :]
# # front_side = arr_3d[:, 0, :]
# # right_side = arr_3d[:, :, 0]

# # right_side = arr_3d[:, :, 0]
# # right_side = arr_3d[:, :, 1]
# # right_side = arr_3d[:, :, 2]

# # print(top_side)
# # # Rotate the right side by 90 degrees
# rotated_right_side = np.rot90(right_side, k=1)

# # Assign the rotated right side back to the array
# arr_3d[:, :, -1] = rotated_right_side


# print("=============================")
# print(arr_3d)
