import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# CUBE_SIZE = 200
CUBE_SIZE = 150
SQUARE_SIZE = CUBE_SIZE // 3
FPS = 30

# Colors for cube faces
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 121, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Cube initialization: 6 faces with 3x3 grids
cube =  {
	"U": [[YELLOW] * 3 for _ in range(3)],  # Up
	"D": [[WHITE] * 3 for _ in range(3)], # Down
	"F": [[RED] * 3 for _ in range(3)],    # Front
	"B": [[ORANGE] * 3 for _ in range(3)], # Back
	"L": [[BLUE] * 3 for _ in range(3)],   # Left
	"R": [[GREEN] * 3 for _ in range(3)],  # Right
}

# Draw a face of the cube
def draw_face(screen, face, x, y):
	for i, row in enumerate(face):
		for j, color in enumerate(row):
			rect = pygame.Rect(x + j * SQUARE_SIZE, y + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
			pygame.draw.rect(screen, color, rect)
			pygame.draw.rect(screen, BLACK, rect, 1)  # Border

# Main loop
def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Rubik's Cube")
	clock = pygame.time.Clock()
	
	running = True
	while running:
		screen.fill(BLACK)
		
		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		u = 50
		l = 100
		# s = 200
		s = CUBE_SIZE
		# Draw the cube faces (simple flat layout)
		draw_face(screen, cube["U"], l+s, u)  # Up face
		draw_face(screen, cube["F"], l+s, u+s) # Front face
		draw_face(screen, cube["D"], l+s, u+(2*s)) # Down face
		draw_face(screen, cube["L"], l, u+s) # Left face
		draw_face(screen, cube["R"], l+(2*s), u+s) # Right face
		draw_face(screen, cube["B"], l+(3*s), u+s) # Back face

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()






# from cube import Cube

# cube = Cube(2)
# print(cube)

# # cube.rotate_r()
# # cube.rotate_r(index_to_move=0)
# # cube.rotate_r(index_to_move=1)
# # cube.rotate_r(index_to_move=2)

# cube.rotate_all_r()

# print(cube)