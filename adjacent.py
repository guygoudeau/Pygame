adj = 0

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.pos = [x,y]
		
	def adjacent(self, other):
		if (other.pos[0] == self.pos[0]-1 or other.pos[0] == self.pos[0]+1):
			adj = 1
		if (other.pos[1] == self.pos[1]-1 or other.pos[1] == self.pos[1]+1):
			adj = 1
		

node1 = Node(1, 2)
node2 = Node(2, 2)

node1.adjacent(node2)
print adj