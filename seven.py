import numpy as np
import copy


# rotation R
# f -> u
# u -> b
# b -> d
# d -> f
# a["f"], a["u"], a["b"], a["d"] = a["u"], a["b"], a["d"], a["f"] #rev
# a["u"], a["b"], a["d"], a["f"] = a["f"], a["u"], a["b"], a["d"]

# rotation L
# f -> d
# u -> f
# b -> u
# d -> b
# a["f"], a["u"], a["b"], a["d"] = a["d"], a["f"], a["u"], a["b"] #rev
# a["d"], a["f"], a["u"], a["b"] = a["f"], a["u"], a["b"], a["d"]

# rotation U
# f -> l
# l -> b
# b -> r
# r -> f
# a["f"], a["l"], a["b"], a["r"] = a["l"], a["b"], a["r"], a["f"] #rev
# a["l"], a["b"], a["r"], a["f"] = a["f"], a["l"], a["b"], a["r"]

# rotation D
# f -> r
# l -> f
# b -> l
# r -> b
# a["f"], a["l"], a["b"], a["r"] = a["r"], a["f"], a["l"], a["b"] #rev
# a["r"], a["f"], a["l"], a["b"] = a["f"], a["l"], a["b"], a["r"]

# rotation F
# u -> r
# r -> d
# d -> l
# l -> u
# a["u"], a["r"], a["d"], a["l"] = a["r"], a["d"], a["l"], a["u"] #rev
# a["r"], a["d"], a["l"], a["u"] = a["u"], a["r"], a["d"], a["l"]


# rotation B
# u -> l
# r -> u
# d -> r
# l -> d
# a["u"], a["r"], a["d"], a["l"] = a["l"], a["u"], a["r"], a["d"] #rev
# a["l"], a["u"], a["r"], a["d"] = a["u"], a["r"], a["d"], a["l"]



def rotate_u(arr, k=1):
    r=0
    aaa = arr[:, r, :]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["l"], aaa[i][j]["b"], aaa[i][j]["r"], aaa[i][j]["f"] =\
            aaa[i][j]["f"], aaa[i][j]["l"], aaa[i][j]["b"], aaa[i][j]["r"]

    aaa = np.rot90(aaa, k=k)
    arr[:, r, :] = aaa

def rotate_d(arr, k=1):
    r=-1
    aaa = arr[:, r, :]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["r"], aaa[i][j]["f"], aaa[i][j]["l"], aaa[i][j]["b"] =\
            aaa[i][j]["f"], aaa[i][j]["l"], aaa[i][j]["b"], aaa[i][j]["r"]

    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[:, r, :] = aaa

def rotate_l(arr, k=1):
    r=0
    aaa = arr[:, :, r]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["d"], aaa[i][j]["f"], aaa[i][j]["u"], aaa[i][j]["b"] =\
            aaa[i][j]["f"], aaa[i][j]["u"], aaa[i][j]["b"], aaa[i][j]["d"]

    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[:, :, r] = aaa

def rotate_r(arr, k=1):
    r=-1
    aaa = arr[:, :, r]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["u"], aaa[i][j]["b"], aaa[i][j]["d"], aaa[i][j]["f"] =\
            aaa[i][j]["f"], aaa[i][j]["u"], aaa[i][j]["b"], aaa[i][j]["d"]

    aaa = np.rot90(aaa, k=k)
    arr[:, :, r] = aaa

def rotate_f(arr, k=1):
    r=0
    aaa = arr[r, :, :]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["r"], aaa[i][j]["d"], aaa[i][j]["l"], aaa[i][j]["u"] =\
            aaa[i][j]["u"], aaa[i][j]["r"], aaa[i][j]["d"], aaa[i][j]["l"]

    aaa = np.rot90(aaa, k=k, axes=(1,0))
    arr[r, :, :] = aaa

def rotate_b(arr, k=1):
    r=-1
    aaa = arr[r, :, :]

    for i in range(len(aaa)):
        for j in range(len(aaa[i])):
            aaa[i][j]["l"], aaa[i][j]["u"], aaa[i][j]["r"], aaa[i][j]["d"] =\
            aaa[i][j]["u"], aaa[i][j]["r"], aaa[i][j]["d"], aaa[i][j]["l"]

    aaa = np.rot90(aaa, k=k)
    arr[r, :, :] = aaa



array = np.array([
    [
        [{"u": "yellow", "d": None, "l": "blue", "r": None, "f": "red", "b": None},
        {"u": "yellow", "d": None, "l": None, "r": None, "f": "red", "b": None},
        {"u": "yellow", "d": None, "l": None, "r": "green", "f": "red", "b": None}],

        [{"u": None, "d": None, "l": "blue", "r": None, "f": "red", "b": None},
        {"u": None, "d": None, "l": None, "r": None, "f": "red", "b": None},
        {"u": None, "d": None, "l": None, "r": "green", "f": "red", "b": None}],
        
        [{"u": None, "d": "white", "l": "blue", "r": None, "f": "red", "b": None},
        {"u": None, "d": "white", "l": None, "r": None, "f": "red", "b": None},
        {"u": None, "d": "white", "l": None, "r": "green", "f": "red", "b": None}]
    ],
    
    [
        [{"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": None}, 
        {"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": None}, 
        {"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": None}],

        [{"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": None}, 
        {"u": None, "d": None, "l": None, "r": None, "f": None, "b": None}, 
        {"u": None, "d": None, "l": None, "r": "green", "f": None, "b": None}],

        [{"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": None}, 
        {"u": None, "d": "white", "l": None, "r": None, "f": None, "b": None}, 
        {"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": None}]
    ],
    
    [
        [{"u": "yellow", "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}, 
        {"u": "yellow", "d": None, "l": None, "r": None, "f": None, "b": "orange"}, 
        {"u": "yellow", "d": None, "l": None, "r": "green", "f": None, "b": "orange"}],
        
        [{"u": None, "d": None, "l": "blue", "r": None, "f": None, "b": "orange"}, 
        {"u": None, "d": None, "l": None, "r": None, "f": None, "b": "orange"}, 
        {"u": None, "d": None, "l": None, "r": "green", "f": None, "b": "orange"}],
        
        [{"u": None, "d": "white", "l": "blue", "r": None, "f": None, "b": "orange"}, 
        {"u": None, "d": "white", "l": None, "r": None, "f": None, "b": "orange"}, 
        {"u": None, "d": "white", "l": None, "r": "green", "f": None, "b": "orange"}]
    ]
])


arr = copy.deepcopy(array)


count = 0
proceed = True


# while proceed or (array != arr).any():
#     if proceed: proceed = False
#     rotate_r(arr)
#     # print("=======================")
#     # print(arr)
#     count+=1

#     if count > 100:
#         break



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

#     if count > 100:
#         break




# total count is (420*3) = 1260
# proves that the small cubes also change orientation when a side is rotated
# if they don't change orientation, count will be 420
# if they change orientation, count will be 1260
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
