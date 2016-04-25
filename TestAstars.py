import pygame
from Astars import *

def main():

	searchSpace = [] # create the search space to look through
	walls = ((5, 0), (0, 1), (1, 1), (5, 1), (3, 2), (1, 3), (2, 3), (5, 3), (1, 4), (4, 4), (1, 5))
	for x in range(6):
		for y in range(6):
			if (x, y) in walls:
				reachable = False
			else:
				reachable = True
			n = Node(x, y, reachable)
			searchSpace.append(n)
	start = searchSpace[0] # starting point
	start.IsStart = True
	goal = searchSpace[35] # end goal
	goal.IsGoal = True
		
	pygame.init() # Initialize pygame
	WINDOW_SIZE = [255, 255] # Set the HEIGHT and WIDTH of the screen
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Astar") # Set title of screen
	done = False # Loop until the user clicks the close button.
	clock = pygame.time.Clock() # Used to manage how fast the screen updates

	# -------- Main Program Loop -----------
	while not done:
		for event in pygame.event.get():  # User did something
			if event.type == pygame.QUIT:  # If user clicked close
				done = True	 # Flag that we are done so we exit this loop

		screen.fill(black) # Set the screen background

		for i in searchSpace:
			i.draw(screen, white)

		clock.tick(60) # Limit to 60 frames per second

		pygame.display.flip() # Go ahead and update the screen with what we've drawn.

	pygame.quit() # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.

main()