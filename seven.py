from cube import Cube

cube = Cube(3)
print(cube)

# cube.rotate_r()
# cube.rotate_r(index_to_move=0)
# cube.rotate_r(index_to_move=1)
# cube.rotate_r(index_to_move=2)

cube.rotate_all_r()

print(cube)