# from functools import partial

# def one(a, b):
# 	return a+b

# two = partial(one, b="aa", a="bb")
# # print(two(a="bb"))

# print(two(b="11", a="22"))


from cube import Cube

# cube = Cube(2)
cube = Cube(3)
# cube = Cube(4)
print(cube)

proceed = True
count = 0
while not cube.solved() or proceed:
	if proceed: proceed = False


	cube.rotate_r(times_to_move=1)
	count+=1
	# cube.rotate_l(times_to_move=3)
	# cube.rotate_l(-1)
	# count+=1
	cube.rotate_all_u()


	if count%4==0:
		# print(count, "=======")
		cube.rotate_u(times_to_move=1)
		cube.rotate_d(times_to_move=1)
	


# 	cube.rotate_r()
# 	count+=1
# 	cube.rotate_l(-1)
# 	count+=1



# 	# cube.rotate_r()
# 	# count+=1
# 	# cube.rotate_b()
# 	# count+=1
# 	# cube.rotate_l()
# 	# count+=1
# 	# cube.rotate_f()
# 	# count+=1



# 	# cube.rotate_u()
# 	# count+=1
# 	# cube.rotate_r()
# 	# count+=1
# 	# cube.rotate_b()
# 	# count+=1


print(count)




# cube.rotate_r(index_to_move=1)
# cube.rotate_r(index_to_move=2)
# cube.rotate_r(index_to_move=3)
# cube.rotate_r(times_to_move=1)





# cube.rotate_r(index_to_move=0)
# cube.rotate_r(index_to_move=1)
# cube.rotate_r(index_to_move=2)

# cube.rotate_r()
# cube.rotate_l(-1)
# cube.rotate_all_u()

# cube.orient_cubelets()

# cube.rotate_r(index_to_move=2)
# cube.rotate_l(-1)
print(cube.solved())



# cube.rotate_r(index_to_move=2)
# cube.rotate_r()
print(cube)