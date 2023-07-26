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


arr = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])

aaa = np.copy(arr)
bbb = np.array([[[3, 12, 21], [4, 5, 6], [7, 8, 9]], [[2, 11, 20], [13, 14, 15], [16, 17, 18]], [[1, 10, 19], [22, 23, 24], [25, 26, 27]]])
rotate_u(aaa)
assert((aaa==bbb).all())

aaa = np.copy(arr)
bbb = np.array([[[1, 2, 3], [4, 5, 6], [25, 16, 7]], [[10, 11, 12], [13, 14, 15], [26, 17, 8]], [[19, 20, 21], [22, 23, 24], [27, 18, 9]]])
rotate_d(aaa)
assert((aaa==bbb).all())

aaa = np.copy(arr)
bbb = np.array([[[19, 2, 3], [10, 5, 6], [1, 8, 9]], [[22, 11, 12], [13, 14, 15], [4, 17, 18]], [[25, 20, 21], [16, 23, 24], [7, 26, 27]]])
rotate_l(aaa)
assert((aaa==bbb).all())

aaa = np.copy(arr)
bbb = np.array([[[1, 2, 9], [4, 5, 18], [7, 8, 27]], [[10, 11, 6], [13, 14, 15], [16, 17, 24]], [[19, 20, 3], [22, 23, 12], [25, 26, 21]]])
rotate_r(aaa)
assert((aaa==bbb).all())

aaa = np.copy(arr)
bbb = np.array([[[7, 4, 1], [8, 5, 2], [9, 6, 3]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
rotate_f(aaa)
assert((aaa==bbb).all())

aaa = np.copy(arr)
bbb = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[21, 24, 27], [20, 23, 26], [19, 22, 25]]])
rotate_b(aaa)
assert((aaa==bbb).all())
