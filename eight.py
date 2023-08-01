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


def orient_cubelets(arr, l, r):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j][l[0]], arr[i][j][l[1]], arr[i][j][l[2]], arr[i][j][l[3]] =\
            arr[i][j][r[0]], arr[i][j][r[1]], arr[i][j][r[2]], arr[i][j][r[3]]


def rotate_u(arr, k=1):
    r=0
    cube_slice = arr[:, r, :]
    orient_cubelets(cube_slice, "lbrf", "flbr")
    cube_slice = np.rot90(cube_slice, k=k)
    arr[:, r, :] = cube_slice

def rotate_d(arr, k=1):
    r=-1
    cube_slice = arr[:, r, :]
    orient_cubelets(cube_slice, "rflb", "flbr")
    cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
    arr[:, r, :] = cube_slice

def rotate_l(arr, k=1):
    r=0
    cube_slice = arr[:, :, r]
    orient_cubelets(cube_slice, "dfub", "fubd")
    cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
    arr[:, :, r] = cube_slice

def rotate_r(arr, k=1):
    r=-1
    cube_slice = arr[:, :, r]
    orient_cubelets(cube_slice, "ubdf", "fubd")
    cube_slice = np.rot90(cube_slice, k=k)
    arr[:, :, r] = cube_slice

def rotate_f(arr, k=1):
    r=0
    cube_slice = arr[r, :, :]
    orient_cubelets(cube_slice, "rdlu", "urdl")
    cube_slice = np.rot90(cube_slice, k=k, axes=(1,0))
    arr[r, :, :] = cube_slice

def rotate_b(arr, k=1):
    r=-1
    cube_slice = arr[r, :, :]
    orient_cubelets(cube_slice, "lurd", "urdl")
    cube_slice = np.rot90(cube_slice, k=k)
    arr[r, :, :] = cube_slice



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



rotate_f(arr)
rotate_r(arr)
rotate_b(arr)
rotate_l(arr)



def group_sides(arr):
    orr = {"f": [], "b": [], "u": [], "d": [], "l": [], "r": []}

    ffff = arr[0,:,:]
    orr["f"] = [[f["f"] for f in ff] for ff in ffff]

    bbbb = arr[-1,:,:]
    bbbb = np.fliplr(bbbb)
    orr["b"] = [[b["b"] for b in bb] for bb in bbbb]

    uuuu = arr[:,0,:]
    uuuu = np.flipud(uuuu)
    orr["u"] = [[u["u"] for u in uu] for uu in uuuu]

    dddd = arr[:,-1,:]
    orr["d"] = [[d["d"] for d in dd] for dd in dddd]

    llll = arr[:,:,0]
    llll = np.rot90(llll, k=1, axes=(1,0))
    orr["l"] = [[l["l"] for l in ll] for ll in llll]

    rrrr = arr[:,:,-1]
    rrrr = np.rot90(rrrr, k=1)
    rrrr = np.flipud(rrrr)
    orr["r"] = [[r["r"] for r in rr] for rr in rrrr]

    return orr



def repr(arr):
    orr = group_sides(arr)
    ntl = {"yellow": "y", "red": "r", "green": "g", "orange": "o", "blue": "b", "white": "w", None: " "}


    rep = ""
    for i in range(3):
        # print(" ", end="")
        # print(*["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["u"]]], end="|\n", sep="|")

        rep += " "
        rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["u"]]])
        rep += "|\n"        
    for i in range(3):
        # print("|", end="")
        # print(*["".join([ntl[k[i][j]] for j in range(3)]) for k in [orr["l"], orr["f"], orr["r"], orr["b"]]], end="|\n", sep="|")

        rep += "|"
        rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [orr["l"], orr["f"], orr["r"], orr["b"]]])
        rep += "|\n"
    for i in range(3):
        # print(" ", end="")
        # print(*["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["d"]]], end="|\n", sep="|")

        rep += " "
        rep += "|".join(["".join([ntl[k[i][j]] for j in range(3)]) for k in [[[None for _ in range(3)] for _ in range(3)], orr["d"]]])
        rep += "|\n"

    return rep

a = repr(arr)

print("======================")
print(a)
