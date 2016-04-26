import pygame
from Astars import *

def main():

	searchSpace = [] # create the search space to look through
	walls = ((5, 0), (0, 1), (1, 1), (5, 1), (3, 2), (1, 3), (2, 3), (5, 3), (1, 4), (4, 4), (1, 5)) # create walls
	for x in range(6): # 6 rows
		for y in range(6): # 6 columns
			if (x, y) in walls: # if a node's x and y is in the walls list
				reachable = False # it's unreachable
			else: # else if a node's x and y is not in the walls lsit
				reachable = True # it's reachable
			n = Node(x, y, reachable)
			searchSpace.append(n)
	start = searchSpace[0] # starting point
	start.IsStart = True
	goal = searchSpace[35] # end goal
	goal.IsGoal = True	
	
	pygame.init() # Initialize pygame
	WINDOW_SIZE = [255, 255] # Set the HEIGHT and WIDTH of the screen
	screen = pygame.display.set_mode(WINDOW_SIZE) # set screen equal to window size
	pygame.display.set_caption("Astar") # Set title of screen
	done = False # Loop until the user clicks the close button.
	clock = pygame.time.Clock() # Used to manage how fast the screen updates
	
	screen.fill(black) # Set the screen background
		
	for i in searchSpace: # for every reachable node in the search space
		i.draw(screen, white) # color them white

	As = AStar(searchSpace, start, goal) # Create an AStar
	#As.init_grid() # initialize the grid
	As.process(screen) # Call the process for the algorithm
	
	#for n in searchSpace:
		#print n.parent
		
	# -------- Main Program Loop -----------
	while not done:
		for event in pygame.event.get():  # User did something
			if event.type == pygame.QUIT:  # If user clicked close
				done = True	 # Flag that we are done so we exit this loop

		clock.tick(60) # Limit to 60 frames per second

		pygame.display.flip() # Go ahead and update the screen with what we've drawn.

	pygame.quit() # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.

main() # call main