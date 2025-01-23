import pygame
import sys

CUBE_SIZE = 1

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FACE_SIZE = 150
SQUARE_SIZE = FACE_SIZE // CUBE_SIZE
FPS = 30

# Colors for cube faces
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 121, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

top_margin = 50
left_margin = 100

# state = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
state = "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo"

# state = "yyyybbbbrrrrggggoooowwww"
# state = "yryrbbbbrwrwggggyoyowowo"

colors = {"y": YELLOW, "b": BLUE, "r": RED, "g": GREEN ,"o": ORANGE, "w": WHITE}



from cube import Cube
cube = Cube(CUBE_SIZE)

# import attridict
# cube = attridict(state=state)


def draw_from_state(screen):
	for i in range(CUBE_SIZE):
		aaa = cube.state[i*CUBE_SIZE:(i+1)*CUBE_SIZE]
		for j, a in enumerate(aaa):
			color = colors[a]
			rect = pygame.Rect(left_margin + FACE_SIZE + j * SQUARE_SIZE, top_margin + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
			pygame.draw.rect(screen, color, rect)
			pygame.draw.rect(screen, BLACK, rect, 1)


	for i in range(CUBE_SIZE):
		for f in range(4):
			aaa = cube.state[(CUBE_SIZE+i+CUBE_SIZE*f)*CUBE_SIZE:(CUBE_SIZE+i+CUBE_SIZE*f+1)*CUBE_SIZE]
			for j, a in enumerate(aaa):
				color = colors[a]
				rect = pygame.Rect(left_margin + (f*FACE_SIZE) + j * SQUARE_SIZE, top_margin + FACE_SIZE + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
				pygame.draw.rect(screen, color, rect)
				pygame.draw.rect(screen, BLACK, rect, 1)


	for i in range(CUBE_SIZE):
		aaa = cube.state[(i+(CUBE_SIZE*5))*CUBE_SIZE:(i+(CUBE_SIZE*5)+1)*CUBE_SIZE]
		for j, a in enumerate(aaa):
			color = colors[a]
			rect = pygame.Rect(left_margin + FACE_SIZE + j * SQUARE_SIZE, top_margin + (2*FACE_SIZE) + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
			pygame.draw.rect(screen, color, rect)
			pygame.draw.rect(screen, BLACK, rect, 1)


# Main loop
def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Rubik's Cube")
	# clock = pygame.time.Clock()
	
	running = True
	while running:
		screen.fill(BLACK)
		
		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print("click")
				mouse_pos = event.pos
				cube.rotate_r(index_to_move=0)


		draw_from_state(screen)

		pygame.display.flip()
		# clock.tick(FPS)

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
