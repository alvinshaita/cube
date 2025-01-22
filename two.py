"bfs meet in the middle"

from cube import Cube
# import copy
import time

state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
# state = "oggoyrbbryyrbbbwwwyrgyrwbrwyyoggwggwyyboowoogrgorworbb"
# cube = Cube()


# two yellow poining opposite sides
# state = "yyyyyyryrbbybbbbbbbrgrrrrrryggggggggooooooooowwwwwwwww"

# two yellow pointing forward
# state = "yyyyyybygbbrbbbbbbyryrrrrrrrggggggggooooooooowwwwwwwww"
# print(cube)




# cube = Cube()
# state = "gggyyryyrrbbybbybbrrwrrwrrwggoggwggwyyyoooooowwowwobbb"

# cube = Cube(3, state)
# cube = Cube(3)
cube = Cube(2)

# cube.rotate_r()
# cube.rotate_b()
# cube.rotate_b(-1)



# cube_B = Cube(3)
cube_B = Cube(2)



# for i in range(4):
for i in range(2):
	cube.rotate_u(1)
	cube.rotate_r(-1)
	cube.rotate_u(-1)
	cube.rotate_r(1)

cube.rotate_f(1)

# for i in range(2):
for i in range(4):
	cube.rotate_u(1)
	cube.rotate_r(-1)
	cube.rotate_u(-1)
	cube.rotate_r(1)

cube.rotate_f(3)



# 2x2 699.4401s -> 11.65mins
# 3x3 4068.1043s -> 1hr 7.8 mins
# cube.rotate_l()
# cube.rotate_f()
# cube.rotate_r()
# cube.rotate_b()



print(cube)
print(cube.state)
cube.path = []


# a = cube.copy()
# print(cube == a)
# a.rotate_r()
# print(cube == a)
# a.rotate_r(-1)
# print(cube == a)
# print(cube.path)
# print(a.path)
# b = set([cube, a])
# b = [cube]
# print(a in b)
# # print(b)



visited_A = []
todo_A = [cube]

visited_B = []
todo_B = [cube_B]


found_end = False
found_middle = False


start = time.time()
while todo_A and todo_B:
	aaa = todo_A.pop(0)
	bbb = todo_B.pop(0)
	# bbb = todo_B[0]

	# gen = len(aaa.path)
	print("generation A:", len(aaa.path), aaa.path)
	print("generation B:", len(bbb.path), bbb.path)

	visited_A.append(aaa)
	visited_B.append(bbb)
	

	if aaa.solved():
		stop = time.time()
		print("AAA Time taken:", stop - start)
		found_end = True
		# print(aaa)
		# print(aaa.to_string())
		print(aaa.path)
		break

	if bbb.state == cube.state:
		stop = time.time()
		print("BBB Time taken:", stop - start)
		found_end = True
		# print(bbb)
		# print(bbb.to_string())
		print(bbb.path)
		break


	if aaa in visited_B:
		print("yyyyyyyyyyy - visited by b")
		y = [i for i in visited_B if i == aaa]
		print("yyy --------")
		print("aaa path", aaa.path)
		print("bbb path", y[0].path)
		print(aaa.path, "+ inverse of:", y[0].path[::-1])
		found_middle = True
		break

	if bbb in visited_A:
		print("xxxxxxxxxxxxxxx - visited by a")
		x = [i for i in visited_A if i == bbb]
		# print("xxx", x[0].path, bbb.path)
		print("xxx --------")
		print("aaa path", x[0].path)
		print("bbb path", bbb.path)
		print(x[0].path, "+ inverse of:", bbb.path[::-1])
		found_middle = True
		break

	# aa = aaa.copy()
	# aa.rotate_u()
	# if aa not in visited_A and aa not in todo_A:
	# 	todo_A.append(aa)
	# bb = bbb.copy()
	# bb.rotate_u()
	# if bb not in visited_B and bb not in todo_B:
	# 	todo_B.append(bb)


	# aa = aaa.copy()
	# aa.rotate_l()
	# if aa not in visited_A and aa not in todo_A:
	# 	todo_A.append(aa)
	# bb = bbb.copy()
	# bb.rotate_l()
	# if bb not in visited_B and bb not in todo_B:
	# 	todo_B.append(bb)

	
	aa = aaa.copy()
	aa.rotate_f()
	if aa not in visited_A and aa not in todo_A:
		todo_A.append(aa)
	bb = bbb.copy()
	bb.rotate_f()
	if bb not in visited_B and bb not in todo_B:
		todo_B.append(bb)
	

	aa = aaa.copy()
	aa.rotate_r()
	if aa not in visited_A and aa not in todo_A:
		todo_A.append(aa)
	bb = bbb.copy()
	bb.rotate_r()
	if bb not in visited_B and bb not in todo_B:
		todo_B.append(bb)

	
	# aa = aaa.copy()
	# aa.rotate_b()
	# if aa not in visited_A and aa not in todo_A:
	# 	todo_A.append(aa)
	# bb = bbb.copy()
	# bb.rotate_b()
	# if bb not in visited_B and bb not in todo_B:
	# 	todo_B.append(bb)

	
	# aa = aaa.copy()
	# aa.rotate_d()
	# if aa not in visited_A and aa not in todo_A:
	# 	todo_A.append(aa)
	# bb = bbb.copy()
	# bb.rotate_d()
	# if bb not in visited_B and bb not in todo_B:
	# 	todo_B.append(bb)


print("Found end:", found_end)
print("Found middle:", found_middle)
