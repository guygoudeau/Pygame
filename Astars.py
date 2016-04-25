import heapq
import pygame as gfx

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

class Node(object):
	def __init__(self, x, y, reachable):
		self.reachable = reachable # is cell not a wall
		self.x = x
		self.y = y
		self.g = 0
		self.h = 0
		self.f = 0
		self.parent = None
		self.color = white
		self.width = 37
		self.height = 37
		self.margin = 5
		self.left = (self.margin + self.width) *  x + self.margin
		self.top = (self.margin + self.height) *  y + self.margin
		self.pos = (x, self.height - y)
		self.IsStart = False
		self.IsGoal = False
		
	def draw(self, screen, color):
		margin = self.margin
		color = white if (self.reachable) else red
		if (self.IsStart == True):
			color = blue
		if (self.IsGoal == True):
			color = green
		gfx.draw.rect(screen, color, (self.left , self.top, self.width, self.height))

class AStar(object):
	def __init__(self, SearchSpace, Start, Goal):
		self.open = []
		heapq.heapify(self.open) #open list heapified to keep node with lowest F at the top
		self.close = set() # closed list is set for fast lookup
		self.nodes = [] # nodes list
		self.grid_height = 6
		self.grid_width = 6
		self.start = Start
		self.goal = Goal
		
	def init_grid(self): # initialize list of nodes
		walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1)) # unreachable nodes
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				if (x, y) in walls:
					reachable = False
				else:
					reachable = True
				self.nodes.append(Node(x, y, reachable))
		self.start = self.get_node(0,0) # starting point
		self.start.IsStart = True
		self.goal = self.get_node(5, 5) # end goal
		self.goal.IsGoal = True
	
	def get_heuristic(self, node): # Heuristic value H: distance between this node and goal multiplied by 10
		return 10 * (abs(node.x - self.goal.x) + abs(node.y - self.goal.y)) # <- manhatten distance
		
	def get_node(self, x, y): # return a node based on x and y coords
		return self.nodes[x * self.grid_height + y]
		
	def get_adjacent_nodes(self, node): # retrieve list of adjacent nodes to a specific node
		nodes = []
		if node.x < self.grid_width-1:
			nodes.append(self.get_node(node.x+1, node.y))
		if node.y > 0:
			nodes.append(self.get_node(node.x, node.y-1))
		if node.x > 0:
			nodes.append(self.get_node(node.x-1, node.y))
		if node.y < self.grid_height-1:
			nodes.append(self.get_node(node.x, node.y+1))
		return nodes
		
	def print_path(self): # print a path if found
		node = self.goal
		while node.parent is not self.start:
			node = node.parent
			print 'path: node: %d,%d' % (node.x, node.y)
			
	def update_node(self, adj, node): # Calculate G, H and F score and set parent node
		adj.g = node.g + 10
		adj.h = self.get_heuristic(adj)
		adj.f = adj.h + adj.g
		adj.parent = node
		
	def process(self): # implement the algorithm
		heapq.heappush(self.open, (self.start.f, self.start)) # add starting node to open list heap
		while len(self.open):
			f, node = heapq.heappop(self.open) # pop node from heap
			self.close.add(node) # add that node to closed list
			if node is self.goal: # if the goal is found print the path and end
				self.print_path()
				break
			adj_nodes = self.get_adjacent_nodes(node) # get the adjacent nodes for current node
			for adj_node in adj_nodes:
				if adj_node.reachable and adj_node not in self.close: # if adj node is reachable and not in closed list
					if (adj_node.f, adj_node) in self.open:
						# if an adjacent node is in open list, check if current path is better
						# than the last one found for this adjacent node
						if adj_node.g > node.g + 10:
							self.update_node(adj_node, node)
					else:
						self.update_node(adj_node, node)
						heapq.heappush(self.open, (adj_node.f, adj_node)) # add adjacent node to open list