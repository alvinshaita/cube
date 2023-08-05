import numpy as np

def rotate_u(arr, k=1):
    r=0
    aaa = arr[:, r, :]
    aaa = np.rot90(aaa, k=k)
    arr[:, r, :] = aaa

def rotate_d(arr, k=1):
    r=-1
    aaa = arr[:, r, :]
    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[:, r, :] = aaa

def rotate_l(arr, k=1):
    r=0
    aaa = arr[:, :, r]
    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[:, :, r] = aaa

def rotate_r(arr, k=1):
    r=-1
    aaa = arr[:, :, r]
    aaa = np.rot90(aaa, k=k)
    arr[:, :, r] = aaa

def rotate_f(arr, k=1):
    r=0
    aaa = arr[r, :, :]
    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[r, :, :] = aaa

def rotate_b(arr, k=1):
    r=-1
    aaa = arr[r, :, :]
    aaa = np.rot90(aaa, k=k)
    arr[r, :, :] = aaa


array = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
# print((arr == arr).all())

arr = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
# print((arr == arr).all())



count = 0
proceed = True
# while proceed or (array != arr).any():
#     if proceed: proceed = False
#     rotate_l(arr)
#     count+=1
#     rotate_r(arr)
#     count+=1
#     rotate_f(arr)
#     count+=1
#     rotate_b(arr)
#     count+=1


while proceed or (array != arr).any():
    if proceed: proceed = False
    rotate_f(arr)
    count+=1
    rotate_r(arr)
    count+=1
    rotate_b(arr)
    count+=1
    rotate_l(arr)
    count+=1



    
print(count)

    # print(proceed, (array != arr).any())
