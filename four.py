from cube import Cube

cube = Cube(4)
print(cube)

# cube.rotate_r()
cube.rotate_r(index_to_move=1)
cube.rotate_r(index_to_move=2)
cube.rotate_r(index_to_move=3)
cube.rotate_r(times_to_move=1)

print(cube.solved())



# cube.rotate_r(index_to_move=2)
# cube.rotate_r()
print(cube)