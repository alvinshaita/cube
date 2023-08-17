"bfs"

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




# for i in range(4):
# 	cube.rotate_u(1)
# 	cube.rotate_r(-1)
# 	cube.rotate_u(-1)
# 	cube.rotate_r(1)

# cube.rotate_f(1)

# for i in range(2):
# 	cube.rotate_u(1)
# 	cube.rotate_r(-1)
# 	cube.rotate_u(-1)
# 	cube.rotate_r(1)

# cube.rotate_f(3)



cube.rotate_l()
cube.rotate_f()


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



visited = []
todo = [cube]
found = False


start = time.time()
while todo:
	ccc = todo.pop(0)

	# gen = len(ccc.path)
	print("generation:", len(ccc.path), ccc.path)
	visited.append(ccc)
	

	if ccc.solved():
		stop = time.time()
		print("Time taken:", stop - start)
		found = True
		# print(ccc)
		# print(ccc.to_string())
		print(ccc.path)
		break


	cc = ccc.copy()
	cc.rotate_u()
	if cc not in visited and cc not in todo:
		todo.append(cc)

	cc = ccc.copy()
	cc.rotate_l()
	if cc not in visited and cc not in todo:
		todo.append(cc)
	
	cc = ccc.copy()
	cc.rotate_f()
	if cc not in visited and cc not in todo:
		todo.append(cc)
	
	cc = ccc.copy()
	cc.rotate_r()
	if cc not in visited and cc not in todo:
		todo.append(cc)
	
	cc = ccc.copy()
	cc.rotate_b()
	if cc not in visited and cc not in todo:
		todo.append(cc)
	
	cc = ccc.copy()
	cc.rotate_d()
	if cc not in visited and cc not in todo:
		todo.append(cc)






	# for k in range(1,4):
	# 	cc = ccc.copy()
	# 	# cc.rotate_u(k)
	# 	# if cc not in visited and cc not in todo:
	# 	# 	todo.append(cc)

	# 	cc = ccc.copy()
	# 	cc.rotate_l(k)
	# 	if cc not in visited and cc not in todo:
	# 		todo.append(cc)
		
	# 	cc = ccc.copy()
	# 	cc.rotate_f(k)
	# 	if cc not in visited and cc not in todo:
	# 		todo.append(cc)
		
	# 	cc = ccc.copy()
	# 	cc.rotate_r(k)
	# 	if cc not in visited and cc not in todo:
	# 		todo.append(cc)
		
	# 	cc = ccc.copy()
	# 	cc.rotate_b(k)
	# 	if cc not in visited and cc not in todo:
	# 		todo.append(cc)
		
	# 	cc = ccc.copy()
	# 	cc.rotate_d(k)
	# 	if cc not in visited and cc not in todo:
	# 		todo.append(cc)





print("Found:", found)
# print(visited)
# print(todo)





# for i in range(4):
# 	cube.rotate_u(1)
# 	cube.rotate_r(-1)
# 	cube.rotate_u(-1)
# 	cube.rotate_r(1)

# cube.rotate_f(1)

# for i in range(2):
# 	cube.rotate_u(1)
# 	cube.rotate_r(-1)
# 	cube.rotate_u(-1)
# 	cube.rotate_r(1)

# cube.rotate_f(3)


# print(cube)
# print(cube.state)
# print(cube.solution)
# # print(cube.path)
# print(cube.solved())

# ltf = {"u": cube.rotate_u, "l": cube.rotate_l, "f": cube.rotate_f, "r": cube.rotate_r, "b": cube.rotate_b, "d": cube.rotate_d}
# cpath = cube.path.copy()
# for i,j in cpath[::-1]:
# 	ltf[i](-j)


# print(cube)
# print(cube.state)
# print(cube.solution)
# print(cube.solved())



