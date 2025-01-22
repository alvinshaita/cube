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

# state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
state = "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo"


colors = {"y": YELLOW, "b": BLUE, "r": RED, "g": GREEN ,"o": ORANGE, "w": WHITE}

def draw_from_state(screen):
	u = 50
	l = 100
	# s = 200
	s = CUBE_SIZE

	# # Draw the cube faces (simple flat layout)
	draw_state_face(screen, state[:9], l+s, u)
	draw_state_face(screen, state[9:18], l, u+s)
	draw_state_face(screen, state[18:27], l+s, u+s)
	draw_state_face(screen, state[27:36], l+(2*s), u+s)
	draw_state_face(screen, state[36:45], l+(3*s), u+s)
	draw_state_face(screen, state[45:54], l+s, u+(2*s))


def draw_state_face(screen, face_state, x, y):
	face = [[colors[i] for i in face_state[j*3:(j*3)+3]] for j in range(3)]

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


		draw_from_state(screen)

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