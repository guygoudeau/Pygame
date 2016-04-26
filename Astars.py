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
		self.close = [] # closed list is set for fast lookup
		self.nodes = SearchSpace # nodes list
		self.grid_height = 6
		self.grid_width = 6
		self.start = Start
		self.goal = Goal
		self.current = self.start
		
	def init_grid(self): # initialize list of nodes
		walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1)) # unreachable nodes
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				if (x, y) in walls:
					reachable = False
					n = Node(x,y, False)
				else:
					reachable = True
					n = Node(x,y,True)
				self.nodes.append(n)
		self.start = self.get_node(0,0) # starting point
		self.start.IsStart = True	
		self.goal.IsGoal = True
		
	def manhatten(self, node): # Heuristic value H: distance between this node and goal multiplied by 10
		return 10 * (abs(node.x - self.goal.x) + abs(node.y - self.goal.y)) # <- manhatten distance
		
	def diagonal(self, node):
		xDistance = abs(node.x - self.goal.x)
		yDistance = abs(node.x - self.goal.x)
		if (xDistance > yDistance):
			return 14*yDistance + 10*(xDistance-yDistance)
		else:
			return 14*xDistance + 10*(yDistance-xDistance)
		
	def get_node(self, x, y): # return a node based on x and y coords
		return self.nodes[x * self.grid_height + y]
		
	def get_adjacent_nodes(self, node): # retrieve list of adjacent nodes to a specific node
		nodes = []
		if node.reachable == True:
			if node.x < self.grid_width-1:
				nodes.append(self.get_node(node.x+1, node.y))
			if node.y > 0:
				nodes.append(self.get_node(node.x, node.y-1))
			if node.x > 0:
				nodes.append(self.get_node(node.x-1, node.y))
			if node.y < self.grid_height-1:
				nodes.append(self.get_node(node.x, node.y+1))
				
			if node.x < self.grid_width-1 and node.y > 0:
				nodes.append(self.get_node(node.x-1,node.y+1))
			return nodes
		
	def print_path(self): # print a path if found
		node = self.goal
		while node.parent is not self.start:
			node = node.parent
			print 'path: node: %d,%d' % (node.x, node.y)
			
	def draw_path(self, screen):
		n = self.goal
		while n.parent != None:
			gfx.draw.line(screen, red, [n.left,n.top], [n.parent.left,n.parent.top], 5)
			n = n.parent
			
	def update_node(self, adj, node): # Calculate G, H and F score and set parent node
		if adj.reachable == True:
			adj.g = self.calc_g(node, adj)
			adj.h = self.diagonal(adj)
			adj.f = adj.h + adj.g
			adj.parent = node
		
	def calc_g(self, node1, node2):
		if (abs(self.nodes.index(node1) - self.nodes.index(node2)) == 6) or (abs(self.nodes.index(node1) - self.nodes.index(node2)) == 1):
			return 10
		if (abs(self.nodes.index(node1) - self.nodes.index(node2)) == 7) or (abs(self.nodes.index(node1) - self.nodes.index(node2)) == 5):
			return 14
			
	def process(self, screen): # implement the algorithm		
		self.current = self.start
		self.open.append(self.current)
		var = self.get_adjacent_nodes(self.current)
		for i in var:
			if i.reachable == True:
				self.update_node(i, self.current)
				self.open.append(i)
			
		self.open.remove(self.current)
		self.close.append(self.current)
		while len(self.open) != 0:

			self.open.sort(key = lambda x: x.f) # sort by lowest f
			self.current = self.open[0]
			self.open.remove(self.current)
			self.close.append(self.current)
			
			adj_nodes = self.get_adjacent_nodes(self.current) # get the adjacent nodes for current node
			for adj_node in adj_nodes:
				if adj_node.reachable and adj_node not in self.close: # if adj node is reachable and not in closed list
					if adj_node not in self.open:
						self.update_node(adj_node, self.current)
						self.open.append(adj_node)
					else:
						move = self.current.g + self.calc_g(self.current, adj_node)
						if move < adj_node.g:
							self.current.parent = adj_node.parent
							adj_node.g = calc_g(self.current, adj_node)
										
			if self.goal in self.open: # if the goal is found in open list print & draw the path and end
				self.print_path()
				self.draw_path(screen)
				return True
		return False